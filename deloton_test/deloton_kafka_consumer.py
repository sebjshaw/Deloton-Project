import pandas as pd
import os
from confluent_kafka import Consumer
import json
from dotenv import load_dotenv
load_dotenv()


topic = 'deloton'

# Consumer with `confluent_kafka`
c = Consumer({
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'group.id': 'three-musketeers',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('SASL_USERNAME'),
    'sasl.password': os.getenv('SASL_PASSWORD'),
    # 'session.timeout.ms': 6000,
    # 'heartbeat.interval.ms': 1000,
    # 'fetch.wait.max.ms': 6000,
    'auto.offset.reset': 'latest',
    'enable.auto.commit': 'false',
    'max.poll.interval.ms': '86400000',
    'topic.metadata.refresh.interval.ms': "-1",
    # "client.id": 'id-002-005',
})

c.subscribe([topic])

try:
    while True: 
        response = c.poll(0.5)
        if response == None:
            continue
        value = json.loads(response.value())
        print(value)

except KeyboardInterrupt:
        pass