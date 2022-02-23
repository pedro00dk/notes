import datetime
import random
import signal
import sys
import time
from typing import cast

import kafka

consumer = kafka.KafkaConsumer(
    "foo",
    client_id="consumer-python",
    group_id="consumer-foo",
    bootstrap_servers=["localhost:9080", "localhost:9081", "localhost:9082"],
)


def signal_handler(sig: int, frame: object) -> None:
    print("Caught interrupt signal")
    consumer.close(5)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

for message in consumer:
    print(
        f'{message.topic}-{message.partition} key: {message.key and cast(bytes, message.key).decode("utf-8")} key: {message.value and cast(bytes, message.value).decode("utf-8")}'
    )
