import json
import config
import csv
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=config.SERVER,
                         value_serializer=lambda x:json.dumps(x).encode('utf-8'))
 
with open('Signal.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        producer.send(config.TOPIC, row)
    csvfile.close()
