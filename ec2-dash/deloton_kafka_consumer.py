import os
import pandas as pd
from confluent_kafka import Consumer
import json
from dotenv import load_dotenv
load_dotenv()

def create_kafka_consumer() -> Consumer:
    """Creates a Kafka Consumer and subscribes it the topic 'deloton' which is 
    streaming the data 

    Returns:
        Consumer: A consumer class that is subscribed to the topic 'deloton'
    """

    # Consumer class from confluent_kafka 
    c = Consumer({
        'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
        'group.id': 'three-musketeers',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': os.getenv('SASL_USERNAME'),
        'sasl.password': os.getenv('SASL_PASSWORD'),
        'auto.offset.reset': 'latest',
        'enable.auto.commit': 'false',
    })

    topic = 'deloton' # topic that the data is on 
    c.subscribe([topic])

    return c

def stream_data_from_kafka(c: Consumer) -> str:
    """Streams the data and returns the log as a string

    Args:
        c (Consumer): Consumer class from confluent kafka listening to deloton topic

    Returns:
        str: log information in string format 
    """

    response = c.poll(1)
    log = "" # placeholder for the log variable 
    if response != None:
        value = json.loads(response.value())
        log = value['log'] # extracts the information from the dict datatype
        
    return log

def create_entry_to_dataframe(c: Consumer) -> dict:

    """Polls the data stream twice to retrieve both unique log events and returns all the information 
    in one dict

    Args:
        c (Consumer): Consumer class from confluent kafka listening to deloton topic

    Returns:
        dict: returns all log information (form both unique log events) in dict format
    """

    info = {}
    for i in range(2):
        log = stream_data_from_kafka(c)
        if log != "":
            info['datetime'] = log.split(" men")[0]
            stats_str = log.split("O]:")
            stats = stats_str[1].split(" ")
            if 'Ride' in stats:
                info['duration'] = stats[5][:-1]
                info['resistance'] = stats[8][:-1]
            else:
                info['heart_rate'] = stats[5][:-1]
                info['rpm'] = stats[8][:-1]
                info['power'] = stats[11][:-1]

    return info
