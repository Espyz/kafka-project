import config
from kafka import KafkaConsumer
import json
import psycopg2
import datetime as dt


# Подключение к кафке
consumer = KafkaConsumer(config.TOPIC,
                        bootstrap_servers = config.SERVER,
                        group_id = 'test',
                        auto_offset_reset = 'earliest',
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Подключение к базе данных
connection = psycopg2.connect(user="sammy",
                                password="33215033",
                                host="localhost",
                                port="5432",
                                database="sammy")

cursor = connection.cursor()

con_events_tab = """ INSERT INTO events (wheel_id, time, warning)
                                    VALUES (%s,%s,%s)"""

con_idle_events_tab = """ INSERT INTO idle_events (part, wheel_id, start_downtime, end_downtime)
                                    VALUES (%s,%s,%s,%s)"""

e_tab = ['', '', '']


"""
def waiting(part, time):
    sleep(180)
    print(f'проблема не была устранена на {part} участке, снижение производительности началось в {time}')
"""


# Передача данных из кафки в базу данных

for msg in consumer:
    record_to_insert = ['','','','','','','']
    n = 0
    for stroke in msg.value:
        record_to_insert[n] = stroke
        n += 1

    if record_to_insert[0] == '[10003.0]':

        if record_to_insert[1] == '1':
            new_ts = int(round(dt.datetime.strptime(record_to_insert[5], '%d.%m.%Y %H:%M:%S').timestamp()))
            time_event = record_to_insert[5]

        elif record_to_insert[1] == '0' and record_to_insert[1] != e_tab[0] != '':
            try:
                last_ts = int(round(dt.datetime.strptime(record_to_insert[5], '%d.%m.%Y %H:%M:%S').timestamp()))
                if (180 >= last_ts - new_ts >= 39): #and record_to_insert[1] != '1'
                    e_tab[2] = 'Снижение производительности'
                elif 180 < last_ts - new_ts:
                    ie_tab = [record_to_insert[0], e_tab[0], time_event, record_to_insert[5]]
                    print(ie_tab)
                    cursor.execute(con_idle_events_tab, ie_tab)
                    connection.commit()
                    continue
                    
            except Exception as error:
                new_ts = last_ts

            e_tab[1] = str(last_ts - new_ts)
        
            try:
                print(e_tab)
                cursor.execute(con_events_tab, e_tab)
            except Exception:
                e_tab = ['', '', '']
                connection.commit()
                continue
            e_tab = ['', '', '']
            connection.commit()

    if record_to_insert[0] == '[10003:2]':
        e_tab[0] = record_to_insert[1]

connection.close()
