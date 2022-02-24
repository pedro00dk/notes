import datetime
import random
import signal
import sys
import time

import kafka

producer = kafka.KafkaProducer(
    client_id="producer-python", bootstrap_servers=["localhost:10200", "localhost:10201", "localhost:10202"],
)


def signal_handler(sig: int, frame: object) -> None:
    print("Caught interrupt signal")
    producer.close(5)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


while True:
    next_message = {"key": b"python", "value": bytes(str(datetime.datetime.now())[11:19], "utf-8")}
    print("producing:", next_message)
    producer.send("foo", next_message["value"], next_message["key"])
    time.sleep(random.uniform(1, 10))
