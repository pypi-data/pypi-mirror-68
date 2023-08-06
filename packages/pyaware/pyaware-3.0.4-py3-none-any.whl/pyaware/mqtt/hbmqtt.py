import datetime
import json
import logging.handlers
import asyncio
from pyaware import events
import ruamel.yaml
import hbmqtt.client
from hbmqtt.mqtt.constants import QOS_1
from pyaware.mqtt import models, transformations, factories
import pyaware.config
import uuid

log = logging.getLogger(__file__)


# Patch the client to handle reconnect logic
class MQTTClient(hbmqtt.client.MQTTClient):
    def __init__(self, client_id=None, config=None, loop=None):
        self._on_connect = None
        self.uri_gen = None
        self.disconnect_after = 0
        self._on_connect_task = None
        self.connect_params = {}
        super().__init__(client_id, config, loop)

    @property
    def on_connect(self):
        """If implemented, called when the broker responds to our connection
        request."""
        return self._on_connect

    @on_connect.setter
    def on_connect(self, func):
        """ Define the connect callback implementation.

        Expected signature is:
            connect_callback()
        """
        self._on_connect = func

    @asyncio.coroutine
    def connect(self,
                uri=None,
                cleansession=None,
                cafile=None,
                capath=None,
                cadata=None,
                extra_headers=None):
        if extra_headers is None:
            extra_headers = {}
        self.connect_params = {
            "uri": uri,
            "cleansession": cleansession,
            "cafile": cafile,
            "capath": capath,
            "cadata": cadata
        }
        yield from super().connect(uri, cleansession, cafile, capath, cadata, extra_headers)

    @asyncio.coroutine
    def _do_connect(self):
        if self.uri_gen:
            uri = self.uri_gen()
        else:
            uri = self.connect_params["uri"]
        cleansession = self.connect_params["cleansession"]
        cafile = self.connect_params["cafile"]
        capath = self.connect_params["capath"]
        cadata = self.connect_params["cadata"]
        self.session = self._initsession(uri, cleansession, cafile, capath, cadata)
        return_code = yield from self._connect_coro()
        self._disconnect_task = asyncio.ensure_future(self.handle_connection_close(), loop=self._loop)
        if self.disconnect_after:
            async def disconnect_later():
                await asyncio.sleep(self.disconnect_after)
                log.warning("Scheduled mqtt disconnect")
                await self.disconnect()
                log.warning("Scheduled mqtt reconnect")
                await self.reconnect(self.connect_params.get("clean_session", True))

            asyncio.ensure_future(disconnect_later(), loop=self._loop)
        if return_code == 0 and self.on_connect:
            self._on_connect_task = asyncio.ensure_future(self.on_connect(), loop=self._loop)
        return return_code


@events.enable
class Mqtt:
    """
    Class for setting up google mqtt protocol.
    Assumes that Key Certificates are already generated and the device is created with the associated public key
    """

    def __init__(self, config, gateway_config: dict = None, _async: bool = False):
        """
        :param config: Config dictionary. Must have at least the device_id specified
        """
        self.config = config
        self.gateway_config = gateway_config or {}
        self.mqtt_promises = {}
        self.devices = {}
        self.connecting = asyncio.Event()
        self.client = MQTTClient(self.config.client_id,
                                 config={"default_qos": self.config.publish_qos, "auto_reconnect": True,
                                         "reconnect_max_interval": 60,
                                         "reconnect_retries": -1, "keep_alive": self.config.keepalive})
        self.client.uri_gen = self.gen_uri
        if self.config.token_life > 1:
            self.client.disconnect_after = self.config.token_life * 60 - 60
        else:
            self.client.disconnect_after = 0
        self.client.on_connect = self.setup
        self.topic_loggers = {}
        self.log_messages = True
        self.sub_handles = {}

    def add_devices(self, *device_ids):
        """
        Add devices according to gateway configuration device ids
        :param device_ids:
        :return:
        """
        self.devices.update({d_id: Device(self, d_id) for d_id in device_ids if d_id not in self.devices})

    async def setup(self):
        """
        Get config if it exists. Then set up attached devices from the config
        :param device_ids: List of device ids belonging to this client
        :return:
        """
        self.add_devices(self.config.device_id)
        await asyncio.gather(*(dev.setup() for dev in self.devices.values()))

    async def connect(self):
        # ssl._create_default_https_context = ssl._create_unverified_context
        if self.config.authentication_required:
            await self.client.connect(
                uri=f"mqtts://unused:{self.config.jwt_token.decode('utf-8')}@{self.config.host}:{self.config.port}",
                cleansession=self.config.clean_session,
                cafile=self.config.ca_certs_path)
        else:
            await self.client.connect(
                uri=f"mqtt://{self.config.host}:{self.config.port}",
                cleansession=self.config.clean_session)

    def gen_uri(self):
        if self.config.authentication_required:
            return f"mqtts://unused:{self.config.jwt_token.decode('utf-8')}@{self.config.host}:{self.config.port}"
        else:
            return f"mqtt://{self.config.host}:{self.config.port}"

    async def loop(self):
        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Stopping event loop for hbmqtt client {self.config.device_id}")
                break
            try:
                msg = await self.client.deliver_message(timeout=1)
            except asyncio.TimeoutError:
                continue
            except (AttributeError, IndexError):
                await asyncio.sleep(1)
                continue
            except BaseException as e:
                log.exception(e)
                continue
            for sub in self.sub_handles:
                if events.matches_case_sensitive(msg.topic, sub):
                    try:
                        handle = self.sub_handles[sub](msg)
                    except BaseException as e:
                        log.exception(e)

    async def publish(self, topic, payload, qos):
        uid = self.mqtt_log(topic, payload)
        await self.client.publish(topic, payload, qos)
        self.mqtt_log(topic, payload, uid)

    def form_message(self, data: dict, topic_type: str, **kwargs) -> str:
        parsers = self.config.parsers.get(topic_type, {})
        if parsers:
            factory = parsers.get("factory")
            if factory:
                factory = factories.get_factory(factory)
                msg = factory(data=data, **kwargs)
            else:
                msg = data
            for transform in parsers["transforms"]:
                msg = transformations.get_transform(**transform)(msg)
            msg = models.get_model(parsers["model"]).parse_obj(msg).json(exclude_none=True)
        else:
            msg = json.dumps(data)
        return msg

    def mqtt_log(self, topic, payload, mid=None):
        if self.log_messages:
            try:
                mqtt_log = self.topic_loggers[topic]
            except KeyError:
                mqtt_log = logging.getLogger(topic)
                mqtt_log.setLevel(logging.INFO)
                log_dir = pyaware.config.aware_path / "mqtt_log"
                log_dir.mkdir(parents=True, exist_ok=True)
                formatter = logging.Formatter('%(asctime)-15s %(message)s')
                handler = logging.handlers.TimedRotatingFileHandler(
                    log_dir / f"{topic.replace('/', '_')}.log", "h",
                    backupCount=2)
                handler.setFormatter(formatter)
                mqtt_log.addHandler(handler)
                mqtt_log.propagate = False
                self.topic_loggers[topic] = mqtt_log
            if mid:
                mqtt_log.info(f"Resolved {self.config.host} {mid}")
                return
            mid = uuid.uuid4()
            try:
                mqtt_log.info(f"Publishing {self.config.host} {mid}:\n{json.dumps(json.loads(payload), indent=4, sort_keys=True)}")
                return mid
            except:
                mqtt_log.info(f"Publishing {self.config.host} {mid}:\n{payload}")
                return mid

    def publish_telemetry(self, telemetry):
        for dev_id in telemetry:
            if dev_id in self.devices:
                self.devices[dev_id].publish_telemetry(self.parser(telemetry[dev_id]))

    async def subscribe(self, topic, callback, qos):
        await self.client.subscribe([(topic, qos)])
        self.sub_handles[topic] = callback

    async def unsubscribe(self, topic):
        if self.client._connected_state.is_set():
            await self.client.unsubscribe([topic])
            self.sub_handles.pop(topic, None)

    def __getitem__(self, item):
        return self.devices[item]

    def set_telemetry_parser(self, func):
        """
        Set the json parser for telemetry messages
        :param func:
        :return:
        """
        self.parser = func


@events.enable
class Device:
    """
    Abstracted device to keep messaging specific to a device or gateway contained in an object
    """
    device_id = ""

    def __init__(self, mqtt: Mqtt, device_id: str):
        self.mqtt = mqtt
        self.device_id = device_id
        self.base_topic = "/devices/{device_id}/".format(device_id=device_id)
        self.cmds_active = set([])
        if self.mqtt.config.device_id == self.device_id:
            self.is_gateway = True
            self.config = self.mqtt.gateway_config
            if self.config:
                self.mqtt.add_devices(*self.config.get("devices", []))
        else:
            self.is_gateway = False
            self.config = None
        self.evt_setup = asyncio.Event()
        events.subscribe(self.send, topic=f"trigger_send/{self.device_id}")

    def __repr__(self):
        return "<Device {}>".format(self.device_id)

    async def setup(self):
        """
        Set up the topic subscriptions and published topics
        :return:
        """
        while True:
            if pyaware.evt_stop.is_set():
                raise RuntimeError("Pyaware is stopped")
            try:
                await self._setup()
                self.evt_setup.set()
                log.info(f"Setup {self.device_id}")
                break
            except (asyncio.CancelledError, RuntimeError, GeneratorExit):
                raise
            except BaseException as e:
                log.exception(e)
            await asyncio.sleep(1)

    async def _setup(self):
        if self.is_gateway:
            log.info(f"Subscribing {self.device_id}/commands/system/stop")
            await self.mqtt.subscribe(self.base_topic + "commands/system/stop", self.handle_stop, qos=1)
        else:
            await self.mqtt.publish(self.base_topic + "attach",
                                    payload=json.dumps({'authorization': ""}).encode('utf-8'),
                                    qos=QOS_1)
        await self.mqtt.subscribe(self.base_topic + "config", self.handle_config, qos=self.mqtt.config.subscribe_qos)
        await self.mqtt.subscribe(self.base_topic + "errors", self.handle_errors, qos=0)
        await self.mqtt.subscribe(self.base_topic + "commands/#", self.handle_commands,
                                  qos=self.mqtt.config.subscribe_qos)

    async def subscribe(self, topic, callback, qos=0):
        """
        :param topic: Topic after the base topic of /devices/device_id/
        :param callback:
        :param qos:
        :return:
        """
        await self.mqtt.subscribe(self.base_topic + topic, callback, qos=qos)

    async def send(self, *, data: dict, topic_type: str, **kwargs):
        """
        This is the main entry point for publishing data from pyaware triggers.
        It is subscribed to f"trigger_send/{device_id}".
        It should pull out the device destination, the topic and the do the appropriate data transformations for the
        destination
        :param data:
        :param timestamp:
        :return:
        """
        if pyaware.evt_stop.is_set():
            raise RuntimeError("Pyaware is stopped")
        try:
            await asyncio.wait_for(self.evt_setup.wait(), 10)
        except asyncio.TimeoutError:
            log.warning(f"Could not send telemetry from {self} as it is not setup")
            return
        payload = self.mqtt.form_message(data=data, topic_type=topic_type, **kwargs)
        await self.mqtt.publish(self.base_topic + "events/telemetry", payload.encode('utf-8'),
                                qos=self.mqtt.config.publish_qos)

    def publish_state(self, msg):
        """
        This should be a snapshot of the device state. This should be a representation of the device and not a complete
        parameter values static.
        :param msg:
        :return:
        """
        if self.evt_setup.is_set():
            self.mqtt.publish(self.base_topic + "state", payload=msg, qos=self.mqtt.config.publish_qos)
        else:
            log.warning("Could not send telemetry from {} as it is not setup".format(self))

    async def publish_telemetry(self, msg):
        log.debug("Publishing telemetry")
        log.debug(self.mqtt.client)
        if self.evt_setup.is_set():
            await self.mqtt.publish(self.base_topic + "events/telemetry", payload=msg, qos=self.mqtt.config.publish_qos)
            log.debug("Sent telemetry")
        else:
            log.warning("Could not send telemetry from {} as it is not setup".format(self))

    @events.subscribe(topic="mqqt_topic_send")
    async def publish_topic(self, msg, mqtt_topic):
        log.debug(f"Publishing {mqtt_topic}")
        log.debug(self.mqtt.client)
        if self.evt_setup.is_set():
            parsers = self.mqtt.config.parsers.get(mqtt_topic, {})
            if parsers:
                for transform in parsers["transforms"]:
                    msg = transformations.get_transform(**transform)(msg)
                msg = models.get_model(parsers["model"]).parse_obj(msg).json(exclude_none=True)
            mid = self.mqtt.publish(f"{self.base_topic}{mqtt_topic}", payload=msg, qos=self.mqtt.config.publish_qos)
            log.debug(f"Sent {mqtt_topic} {mid}")
        else:
            log.warning(f"Could not send telemetry from {self} as it is not setup")

    # TODO this needs to have a instance ID as any more than one MQTT device will break here (eg. 2 imacs)
    @events.subscribe(topic=f"mqtt_command_response")
    async def publish_command_response(self, data, timestamp: datetime.datetime):
        data["timestamp"] = f"{timestamp.isoformat()}"
        if data["id"] not in self.cmds_active:
            return
        for param, value in data.get("data", {}).items():
            if isinstance(value, datetime.datetime):
                data["data"][param] = f"{value.isoformat()}"
        log.debug("Publishing command response")
        if self.evt_setup.is_set():
            await self.mqtt.publish(self.base_topic + "events/telemetry/commands", payload=json.dumps(data),
                                    qos=self.mqtt.config.publish_qos)
            log.debug("Sent command response")
        else:
            log.warning("Could not send command response from {} as it is not setup".format(self))
        if data["type"] > 1:
            self.cmds_active.remove(data["id"])

    def handle_config(self, mid):
        """
        If the gateway handle config to update devices and set up remaining pyaware config
        :return:
        """
        if self.is_gateway:
            """
            Check if new config is different to the old config
            If so, override config cache present and restart pyaware cleanly
            """
            log.info("Gateway config received: {}".format(mid.data))
            if mid.data:
                new_config = ruamel.yaml.safe_load(mid.data.decode())
                if new_config:
                    if pyaware.config.config_changes(self.mqtt.gateway_config, new_config):
                        with open(pyaware.config.aware_path / "config" / "gateway.yaml", 'w') as f:
                            ruamel.yaml.dump(new_config, f)
                        log.warning("New gateway configuration detected. Stopping process")
                        pyaware.stop()
        else:
            log.info("Device config received: {}".format(mid.data))
            if mid.data:
                self.config = ruamel.yaml.safe_load(mid.data.decode('utf-8'))

    def handle_errors(self, mid):
        log.warning(f"Error received from gcp\n{mid.payload.decode('utf-8')}")

    def handle_commands(self, mid):
        try:
            msg = json.loads(mid.payload.decode('utf-8'))
        except AttributeError:
            # Ignore commands with no payload
            return
        except json.decoder.JSONDecodeError as e:
            log.exception(e)
            return
        self.cmds_active.add(msg["id"])
        pyaware.events.publish(f"mqtt_command/{self.device_id}", data=msg,
                               timestamp=datetime.datetime.utcnow())

    def handle_stop(self, mid):
        pyaware.stop()
