from confluent_kafka import Consumer, KafkaError, KafkaException
import json

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "metrics_group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)
consumer.subscribe(["auth_logs"])


def consume():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            data = json.loads(msg.value().decode("utf-8"))
            print(f"Received message: {data}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    consume()
