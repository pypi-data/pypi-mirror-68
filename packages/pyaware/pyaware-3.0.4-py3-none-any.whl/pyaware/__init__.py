import functools
import inspect
import logging
import argparse
import signal
import json
import platform

from pyaware.auto_update import check_for_updates, update_pyaware
from pyaware.monitor import DeviceMonitor
from pyaware.scheduler import TaskScheduler
from pyaware import cloud, events
from pyaware.config import *

__version__ = "3.0.4"

parser = argparse.ArgumentParser(description="Sets up a minimal pyaware slave for imac to respond to mqtt commands")
parser.add_argument("path", help="Path to the pyaware path that houses config and credentials")

log = logging.getLogger(__name__)
_parent_process = os.getpid()
evt_stop = events.evt_stop

aware_path = os.getenv("AWAREPATH", "")

_stopping = False


def stop():
    global _stopping
    if _stopping:
        raise RuntimeError("Pyaware is stopped")
    os.kill(_parent_process, signal.SIGINT)
    _stopping = True
    raise RuntimeError("Pyaware is stopped")


async def shutdown(signal, comms, loop):
    """Cleanup tasks tied to the service's shutdown."""
    global _stopping
    try:
        log.info(f"Received exit signal {signal.name}...")
        log.info(f"Stopping internal events")
        events.stop()
        log.info("Closing comms connections")
        for name, instance in comms.items():
            if name == "local_broker":
                log.info("Disconnecting MQTT local broker")
                try:
                    instance.disconnect()
                except BaseException as e:
                    log.exception(e)
            if name == "serial":
                log.info("Disconnecting Master Serial Modbus")
                try:
                    instance.disconnect()
                except BaseException as e:
                    log.exception(e)
            if name == "ethernet":
                log.info("Disconnecting Master Ethernet Modbus")
                try:
                    instance.disconnect()
                except BaseException as e:
                    log.exception(e)

        log.info("Cancelling outstanding tasks")
        tasks = [t for t in asyncio.all_tasks() if t is not
                 asyncio.current_task()]

        [task.cancel() for task in tasks]

        log.info(f"Cancelling {len(tasks)} outstanding tasks")
        if tasks:
            done, pending = await asyncio.wait(tasks, timeout=5, return_when=asyncio.ALL_COMPLETED)
            if pending:
                log.info(f"Force stopping event loop but tasks still remain {tasks}")
            else:
                log.info(f"All tasks stopped. Stopping event loop")
        loop.stop()
    finally:
        _stopping = False


class Aware:
    def __init__(self, api_version):
        self.api = api_version
        self.scheduler = TaskScheduler()
        self.devices = DeviceMonitor(self.scheduler)
        self.events = None
        self.setup_signal_handlers()
        self.cloud_client = cloud.get_client(api_version)
        self.cleanup = []

    def run(self):
        self.scheduler.run()

    def stop(self):
        self.scheduler.close()
        self.cloud_client.disconnect()
        for cmd, args, kwargs in self.cleanup:
            try:
                cmd(*args, **kwargs)
            except BaseException as e:
                log.exception(e)

    def setup_signal_handlers(self):
        """
        Capture the termination signals and do a clean exit
        :return:
        """
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)

    def shutdown_handler(self, signum, frame):
        # If we want to do anything on shutdown, such as stop motors on a robot,
        # you can add it here.
        log.warning("External shutdown signal received, initiating close")
        self.stop()
        exit(1)

    def schedule_devices_read(self, period, task_timeout):
        """
        Schedule the device reads to occur. If the task is still running when it is scheduled to run again,
        it will wait until device read is complete to start again or until the task_timeout occurs
        :param period: How often (in seconds) to schedule a task to run.
        :param task_timeout: Time (in seconds) to wait for the entire device reads to complete before cancelling and
        starting the task again
        :return:
        """
        for device in self.devices._devices:
            self.scheduler.create_periodic_task(device.async_read_data, period, timeout=task_timeout)

    def schedule_devices_read_sync(self, period, task_timeout):
        self.scheduler.create_periodic_task(self._sync_read_data, period, timeout=task_timeout)

    async def _sync_read_data(self):
        for device in self.devices._devices:
            await self.scheduler.loop.run_in_executor(None, device.sync_read_data)

    def schedule_report(self, report, period, task_timeout, start_after):
        self.scheduler.create_periodic_task(self.report_device_telemetry, period, timeout=task_timeout,
                                            start_after=start_after, coro_kwargs={"report": report})

    def add_cleanup(self, cmd, *args, **kwargs):
        self.cleanup.append((cmd, args, kwargs))

    async def report_device_telemetry(self, report):
        """
        Get data, report data, publish to cloud
        :return:
        """
        loop = asyncio.get_event_loop()
        data = self.devices.iter_data()
        resp = await loop.run_in_executor(None, report.report, data)
        await loop.run_in_executor(None, self.cloud_client.publish_telemetry, resp)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


async def _main(path, comms):
    events.start()
    try:
        pyaware.config.aware_path = Path(path)
        pyaware.config.config_main_path = pyaware.config.aware_path / "config" / "gateway.yaml"
        config = pyaware.config.load_config(pyaware.config.config_main_path)
        version = config.get("aware_version", "latest")
        if check_for_updates(version):
            update_pyaware(version)

        comms.update(pyaware.config.parse_communication(communication=config["communication"]))

        @pyaware.events.subscribe(topic="topology", in_thread=True)
        def topology(data, timestamp):
            for serial, devices in data.items():
                payload = {
                    "version": 1,
                    "serial": serial,
                    "type": "imac-controller-master",
                    "timestamp": f"{timestamp.isoformat()[:-3]}Z",
                    "children": devices
                }
                device = list(comms["local_broker"].devices.values())[0]
                device.publish_topic(json.dumps(payload), "topology")
    except RuntimeError:
        pass
    except BaseException as e:
        log.exception(e)
        pyaware.stop()


def logging_config():
    import logging.handlers
    global log
    logname = os.path.join(pyaware.aware_path, "AWARE.log")
    formatter = logging.Formatter('%(asctime)-15s %(threadName)-15s '
                                  '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')

    handler = logging.handlers.TimedRotatingFileHandler(logname, when="midnight", backupCount=7)
    handler.setFormatter(formatter)

    screen_handler = logging.StreamHandler()
    screen_handler.setFormatter(formatter)

    log.setLevel(level=logging.INFO)
    log.addHandler(handler)
    log.addHandler(screen_handler)


def main():
    logging_config()
    args = parser.parse_args()
    comms = {}
    loop = asyncio.get_event_loop()
    if platform.system() == "Windows":
        signals = (signal.SIGTERM, signal.SIGINT)
        for s in signals:
            signal.signal(s, lambda s=s: asyncio.create_task(pyaware.shutdown(s, comms, loop)))
    else:
        # May want to catch other signals too
        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        for s in signals:
            loop.add_signal_handler(
                s, lambda s=s: asyncio.create_task(pyaware.shutdown(s, comms, loop)))
    try:
        loop.create_task(_main(args.path, comms))
        loop.run_forever()
    finally:
        loop.close()
        log.info("Successfully shutdown")


def async_swap(f):
    @functools.wraps(f)
    def _wrapped(self, *args, **kwargs):
        if self._async:
            return getattr(self, f"_{f.__name__}_async")(*args, **kwargs)
        else:
            return getattr(self, f"_{f.__name__}_sync")(*args, **kwargs)

    return _wrapped


def async_threaded(f):
    """
    Wraps a function so that when it is called from an asyncio event loop, it runs in a threadpool executor instead
    :param f:
    :return:
    """

    @functools.wraps(f)
    def _wrapped(*args, **kwargs):
        func = functools.partial(f, *args, **kwargs)
        if from_coroutine():
            return asyncio.get_running_loop().run_in_executor(None, func)
        else:
            return func()

    return _wrapped


async def async_wrap(resp):
    if inspect.isawaitable(resp):
        return await resp
    return resp


async def async_call(handle, *args, **kwargs):
    return await async_wrap(handle(*args, **kwargs))


def from_coroutine():
    """
    Checks if function is in an event loop. If so, then blocking code should not be used
    :return:
    """
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False
