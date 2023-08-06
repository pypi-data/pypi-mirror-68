"""
This module is intended to parse configuration files and instantiate the necessary systems within pyaware.
"""
import os
from pkg_resources import parse_version
import ruamel.yaml
import pyaware.devices
import pyaware
import pyaware.devices.definitions
import pyaware.mqtt.config
import pyaware.mqtt.paho
import pyaware.reporting
import deepdiff
import asyncio
from pathlib import Path

aware_path = Path("")
config_main_path = Path("")


def load_config(file_path):
    """
    Load config in its raw form and produce a dictionary, raw
    :param file_path:
    :return: Loaded config, raw data
    """
    try:
        with open(file_path) as f:
            return ruamel.yaml.safe_load(f)
    except FileNotFoundError:
        with open(file_path, 'w'):
            return {}


def save_config(file_path, config):
    """
    Load config in its raw form and produce a dictionary, raw
    :param file_path:
    :return: Loaded config, raw data
    """
    with open(file_path, 'w') as f:
        ruamel.yaml.dump(config, f, default_flow_style=False)


class ConfigChanged(ValueError):
    pass


def config_changes(original, new):
    return deepdiff.DeepDiff(original, new, ignore_order=True)


def aware_version_check(config: dict):
    """
    Parse the gateway meta data to ensure that appropriate requirements are met
    :param config:
    :return:
    """
    # Check aware version
    if parse_version(pyaware.__version__) < parse_version(config["meta_data"]["aware_version"]):
        # TODO self update in separate process and use older cached config (if existing) until update is complete
        # Then kill off process to let the new version start
        raise ValueError("Currently installed pyaware version is not compatible with the config")


def parse_api_version(config: dict):
    return config["meta_data"]["api_version"]


def parse_gateway_config(config: dict):
    """
    Parse a gateway focused config dictionary to produce devices, communication connections, cloud api versions and
    reporting configurations
    :param config:
    :return: dictionary of form
    {
        "comms": dict of form from parse_communication,
        "device_list": list of form from parse_devices,
        "reports": list of form from parse_reports
    """
    comms = parse_communication(config["communication"])
    dev_list = parse_devices(config["devices"], comms)
    reports = parse_reports(config["reports"])
    return {"comms": comms, "device_list": dev_list, "reports": reports}


def parse_modbus_rtu(port, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Asyncronous modbus client
    """
    from pyaware.protocol.modbus import ModbusAsyncSerialClient
    client = ModbusAsyncSerialClient(port, **kwargs)
    return client


def parse_modbus_rtu2(port, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Asyncronous modbus client
    """
    from aiomodbus.serial import ModbusSerialClient
    client = ModbusSerialClient(port, **kwargs)
    asyncio.get_event_loop().create_task(client.connect())
    return client


def parse_modbus_tcp(host, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Partial function that can be called to initiate the object and connection.
    """
    from pyaware.protocol.modbus import ModbusAsyncTcpClient
    client = ModbusAsyncTcpClient(host, **kwargs)
    asyncio.get_event_loop().create_task(client.start())
    return client


def parse_modbus_tcp2(host, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Partial function that can be called to initiate the object and connection.
    """
    from aiomodbus.tcp import ModbusTCPClient
    client = ModbusTCPClient(host, **kwargs)
    asyncio.get_event_loop().create_task(client.connect())
    return client


def parse_imac2_master(**kwargs):
    from pyaware.protocol.imac2.protocol import Imac2Protocol
    return Imac2Protocol(**kwargs)


def parse_modbus_device(**kwargs):
    from pyaware.protocol.modbus import ModbusDevice
    return ModbusDevice(**kwargs)


def parse_mqtt_raw(device_id, **kwargs):
    import uuid
    config = pyaware.mqtt.config.LocalConfig(str(uuid.uuid4()), device_id)
    client = pyaware.mqtt.paho.Mqtt(config)
    client.client_reinit()
    return client


def parse_paho_gcp(**kwargs):
    config = pyaware.config.load_config(aware_path / "config" / "cloud.yaml")
    config = pyaware.mqtt.config.GCPCloudConfig(**config)
    gateway_config = pyaware.config.load_config(aware_path / "config" / "gateway.yaml")
    client = pyaware.mqtt.paho.Mqtt(config, gateway_config)
    client.client_reinit()
    return client


def parse_hbmqtt_gcp(**kwargs):
    import pyaware.mqtt.hbmqtt
    config = pyaware.config.load_config(aware_path / "config" / "cloud.yaml")
    config = pyaware.mqtt.config.GCPCloudConfig(**config)
    gateway_config = pyaware.config.load_config(aware_path / "config" / "gateway.yaml")
    client = pyaware.mqtt.hbmqtt.Mqtt(config, gateway_config)
    asyncio.create_task(client.connect())
    asyncio.create_task(client.loop())
    return client


def parse_hbmqtt_raw(device_id, **kwargs):
    import uuid
    import pyaware.mqtt.hbmqtt
    config = pyaware.mqtt.config.LocalConfig(str(uuid.uuid4()), device_id)
    gateway_config = pyaware.config.load_config(aware_path / "config" / "gateway.yaml")
    client = pyaware.mqtt.hbmqtt.Mqtt(config, gateway_config)
    asyncio.create_task(client.connect())
    asyncio.create_task(client.loop())
    return client


def parse_gmqtt_gcp(**kwargs):
    import pyaware.mqtt.gmqtt
    config = pyaware.config.load_config(aware_path / "config" / "cloud.yaml")
    config = pyaware.mqtt.config.GCPCloudConfig(**config)
    gateway_config = pyaware.config.load_config(aware_path / "config" / "gateway.yaml")
    client = pyaware.mqtt.gmqtt.Mqtt(config, gateway_config)
    asyncio.create_task(client.connect())
    return client


def parse_devices(devices_list: list, comms: dict):
    """
    Parse the devices from config and group them if they share a resource
    :param devices: parsed config["devices"]
    :param comms: result of parse_communication
    :return: list of devices or device groupings that can be added to the scheduler after binding the client
    """
    protocol_group_handlers = {
        "modbus_rtu": {"class": pyaware.devices.ModbusNursery, "handler": "add_devices"}
    }
    device_groups = {}
    devices = []
    for device in devices_list:
        port_id = device["port_id"]
        protocol = comms[port_id]["protocol"]
        device_type = parse_device_type(device["device_type"], device["version"])
        base_class = pyaware.devices.definitions.protocol_map[protocol]
        data_info = pyaware.devices.definitions.build_data_reads(device["parameters"], device_type["data"])
        commands = pyaware.devices.definitions.build_commands()
        dev = base_class(dev_id=device["device_id"], dev_type=device["device_type"], data_info=data_info,
                         **device["device_config"])
        dev.port_id = port_id
        if protocol in protocol_group_handlers:
            # device will need to be grouped
            meta_proto = protocol_group_handlers[protocol]
            if port_id not in device_groups:
                device_groups[port_id] = meta_proto["class"]()
                device_groups[port_id].port_id = port_id
            # Add the device to the group
            getattr(device_groups[port_id], meta_proto["handler"])(dev)
        else:
            # Add the device as it's own group
            devices.append(dev)
    # Return devices as flat list of combined devices and device groups
    devices.extend(device_groups.values())
    return devices


def parse_device_type(device_type: str, version: int = 1):
    with open(os.path.join(pyaware.config.aware_path, "config", "{}.yaml".format(device_type))) as f:
        device_type = ruamel.yaml.safe_load(f)
    if device_type.get("version", -1) != version:
        raise ValueError(
            "Incorrect version of device type config. Found: {}, Expected: {}".format(
                device_type.get("version", -1), version))
    return device_type


def parse_comm_params(comms, instances):
    comms_params = {}
    for k, v, in comms["params"].items():
        if v["type"] == "value":
            comms_params[k] = v["value"]
        elif v["type"] == "ref_comms":
            comms_params[k] = instances[v["value"]]
        elif v["type"] == "ref_path":
            comms_params[k] = aware_path / Path(v["value"])
        elif v["type"] == "ref_device":
            comms_params[k] = Path(pyaware.devices.__file__).parent / Path(v["value"])
        else:
            raise ValueError("No valid type detected in config file")
    return comms_params


def parse_communication(communication: list):
    """
    :param communication:
    :return: dictionary of form
    {
      <id>:
        {
          "protocol": <string>, # eg. modbus_rtu, modbus_tcp
          "handler": handler to call to return the communication type in a connected state
        },
        {...},
      ...,
    }
    """
    protocol_handlers = {
        "modbus_rtu": parse_modbus_rtu,
        "modbus_rtu2": parse_modbus_rtu2,
        "modbus_tcp": parse_modbus_tcp,
        "modbus_tcp2": parse_modbus_tcp2,
        "imac2_gasguard_live": parse_imac2_master,
        "modbus_device": parse_modbus_device,
        "mqtt_raw": parse_mqtt_raw,
        "mqtt_gcp": parse_paho_gcp,
        "hbmqtt_raw": parse_hbmqtt_raw,
        "hbmqtt_gcp": parse_hbmqtt_gcp,
        "gmqtt_gcp": parse_gmqtt_gcp,
    }
    instances = {}
    for comms in communication:
        comms_params = parse_comm_params(comms, instances)
        instances[comms["name"]] = protocol_handlers[comms["type"]](**comms_params)
    return instances


def parse_reports(reports: list):
    """
    Provisional config parsing until the reporting changes
    :param reports:
    :return:
    """
    new_reports = []
    for itm in reports:
        report = getattr(pyaware.reporting, itm["type"])()
        for agg in itm["aggregates"]:
            for k, v in agg.items():
                getattr(report, k)(**v)
        new_reports.append(report)
    return new_reports
