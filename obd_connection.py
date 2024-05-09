import obd
import logging
import sys

logger = logging.getLogger(__name__)


class ObdConnection:
    def __init__(self, portstr, callback, baud=115200):
        self.portstr = portstr
        self.baud = baud
        self.callback = callback
        logger.debug("Portstr: %s" % self.portstr)
        logger.debug("Baud rate: %d" % self.baud)

        self.commands = []
        self.sync_connection = None
        self.async_connection = None

        self.get_commands()
        self.set_watchers()
        self.start()
        logger.info("OBD started")

    def on_response(self, r):
        if r is None or r.value is None or r.command is None:
            return
        self.callback(r.command.name, r.value.magnitude)

    def get_commands(self):
        logger.debug("Open sync connecton to get available commands")
        self.sync_connection = obd.OBD(portstr=self.portstr, baudrate=self.baud)
        if not self.sync_connection.is_connected():
            logger.critical("Could not connect to car")
            sys.exit(1)

        result = self.sync_connection.query(obd.commands.PIDS_A)

        for i in range(len(result.value)):
            if result.value[i]:
                command = obd.commands[1][i + 1]
                logger.info("Added command %s" % command.name)
                self.commands.append(command)
        self.sync_connection.close()

    def set_watchers(self):
        logger.debug("Set watchers")
        self.async_connection = obd.Async(portstr=self.portstr, baudrate=self.baud)
        for command in self.commands:
            if not command.name in ["PIDS_A", "PIDS_B", "PIDS_C"]:
                self.async_connection.watch(command, callback=self.on_response)

    def start(self):
        logger.debug("Start watching")
        self.async_connection.start()
