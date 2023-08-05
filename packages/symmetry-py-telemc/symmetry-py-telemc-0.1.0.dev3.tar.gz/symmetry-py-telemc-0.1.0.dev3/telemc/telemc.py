from typing import Iterator, NamedTuple


class Telemetry(NamedTuple):
    timestamp: str
    value: str
    node: str
    metric: str
    subsystem: str = None


class TelemetrySubscriber:

    def __init__(self, rds, pattern=None) -> None:
        super().__init__()
        self.rds = rds
        self.pattern = pattern or 'telem/*'
        self.pubsub = None

    def run(self) -> Iterator[Telemetry]:
        self.pubsub = self.rds.pubsub()

        try:
            self.pubsub.psubscribe(self.pattern)

            for item in self.pubsub.listen():
                data = item['data']
                if type(data) == int:
                    continue
                channel = item['channel']
                timestamp, value = data.split(' ')
                parts = channel.split('/', maxsplit=3)
                # 'telem', node_id, metric [, subsystem]

                yield Telemetry(timestamp, value, *parts[1:])
        finally:
            self.pubsub.close()

    def close(self):
        if self.pubsub:
            self.pubsub.punsubscribe()
