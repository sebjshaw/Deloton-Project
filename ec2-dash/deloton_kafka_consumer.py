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

def create_log_entry(c: Consumer) -> dict:

    """Polls the data stream twice to retrieve both unique log events and returns all the information 
    in one dict. If the log event contains 'SYSTEM' (i.e. the user info), this information is compiled 
    into a dict and returned instead

    Args:
        c (Consumer): Consumer class from confluent kafka listening to deloton topic

    Returns:
        dict: returns all log information (form both unique log events) in dict format
    """

    info = {}
    info1 = {}
    info2 = {}
    for i in range(2):
        log = stream_data_from_kafka(c) # polls the topic using the stream_data_from_kafka function

        # if the log is the user information then this is compiled and returned 
        if 'SYSTEM' in log:
            data = log.split("EM] ")[1]
            data = data[8:-2].split(',\"')
            for detail in data:
                stat = detail.replace('\"', '').split(':')
                info[stat[0]] = stat[1]

            return info

        # if this is a regular log it is completed twice 
        if 'INFO' in log:
            info['datetime'] = log.split(" men")[0]
            stats_str = log.split("O]:")
            stats = stats_str[1].split(" ")
            if 'Ride' in stats:
                info1['duration'] = stats[5][:-1]
                info1['resistance'] = stats[8][:-1]
            else:
                info2['heart_rate'] = stats[5][:-1]
                info2['rpm'] = stats[8][:-1]
                info2['power'] = stats[11][:-1]

    info = info | info1 | info2 # dictates the format of the final dictionary to be the same every time 
    return info


# really easy way to test is to create a new python file:

# from deloton_kafka_consumer import create_log_entry, create_kafka_consumer
# c = create_kafka_consumer()
# while True:
#     try: 
#         print(create_log_entry(c))
#     except KeyboardInterrupt:
#         pass





