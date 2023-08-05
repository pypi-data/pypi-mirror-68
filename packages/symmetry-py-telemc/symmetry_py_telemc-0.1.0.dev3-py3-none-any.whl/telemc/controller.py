class TelemetryController:
    """
    The telemetry controller is the gateway to get info of and control telemd nodes.
    """

    def __init__(self, rds) -> None:
        super().__init__()
        self.rds = rds

    def get_nodes(self):
        """
        Returns the hosts listening on their respective telemcmd/<hostname> topics.

        :return: a list of hosts, e.g., ['planck', 'heisenberg']
        """
        return [ch.split('/', maxsplit=1)[1] for ch in self._channels()]

    def pause_all(self):
        for ch in self._channels():
            self._send_pause(ch)

    def pause(self, host):
        self._send_pause(self._channel(host))

    def unpause_all(self):
        for ch in self._channels():
            self._send_unpause(ch)

    def unpause(self, host):
        self._send_unpause(self._channel(host))

    def _channels(self):
        return self.rds.pubsub_channels('telemcmd/*')

    def _channel(self, host):
        return f'telemcmd/{host}'

    def _send_pause(self, ch):
        self.rds.publish(ch, 'pause')

    def _send_unpause(self, ch):
        self.rds.publish(ch, 'unpause')
