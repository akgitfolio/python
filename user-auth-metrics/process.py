from confluent_kafka import Consumer, KafkaError, KafkaException
from elasticsearch import Elasticsearch
import json
from collections import deque


response_times_buffer = deque(maxlen=10)


conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "metrics_group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)
consumer.subscribe(["auth_logs"])


es = Elasticsearch("http://localhost:9200")


def compute_rolling_average(response_times):
    return sum(response_times) / len(response_times)


def detect_anomalies(response_time, threshold):
    return response_time > threshold


def process_event(event):

    print("Received event:", event)

    response_times_buffer.append(event["response_time"])

    rolling_avg_response_time = compute_rolling_average(response_times_buffer)
    print("Rolling Average Response Time:", rolling_avg_response_time)

    anomaly_detected = detect_anomalies(event["response_time"], 1.5)
    print("Anomaly Detected:", anomaly_detected)

    es.index(
        index="auth_logs",
        body={
            **event,
            "rolling_avg_response_time": rolling_avg_response_time,
            "anomaly_detected": anomaly_detected,
        },
    )


try:
    while True:
        msg = consumer.poll(timeout=1.0)
        print(msg)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        data = json.loads(msg.value().decode("utf-8"))
        process_event(data)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
