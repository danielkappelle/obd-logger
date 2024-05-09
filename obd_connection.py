import obd


class ObdConnection:
    def __init__(self, portstr, callback, baud=115200):
        self.portstr = portstr
        self.baud = baud
        self.callback = callback

        self.commands = []
        self.sync_connection = None
        self.async_connection = None

        self.get_commands()
        self.set_watchers()
        self.start()
        print("OBD started")

    def on_response(self, r):
        if r is None or r.value is None or r.command is None:
            return
        self.callback(r.command.name, r.value.magnitude)

    def get_commands(self):
        self.sync_connection = obd.OBD(portstr=self.portstr, baudrate=self.baud)
        result = self.sync_connection.query(obd.commands.PIDS_A)

        for i in range(len(result.value)):
            if result.value[i]:
                self.commands.append(obd.commands[1][i + 1])
        self.sync_connection.close()

    def set_watchers(self):
        self.async_connection = obd.Async(portstr=self.portstr, baudrate=self.baud)
        for command in self.commands:
            if not command.name in ["PIDS_A", "PIDS_B", "PIDS_C"]:
                self.async_connection.watch(command, callback=self.on_response)

    def start(self):
        self.async_connection.start()
