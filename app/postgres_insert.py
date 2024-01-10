import json
import time
from confluent_kafka import Consumer, KafkaError
import psycopg2
from psycopg2 import Error
from app.decorators import logger

# Функция для вставки данных в PostgreSQL
@logger
def insert_weather_data(weather_data, connection_params):
    try:
        connection = psycopg2.connect(**connection_params)

        cursor = connection.cursor()

        # Пример запроса для вставки
        insert_query = """INSERT INTO your_table (data_column) VALUES (%s);"""
        record_to_insert = (weather_data['data'],)

        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        print("Weather data inserted successfully")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Функция для запуска Kafka Consumer и обработки сообщений
def run_consumer(duration_seconds=3600):
    start_time = time.time()
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    })
    c.subscribe(['weather_data'])

    try:
        while True:
            current_time = time.time()
            if current_time - start_time > duration_seconds:
                break

            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            weather_data = json.loads(msg.value().decode('utf-8'))
            connection_params = {
                "user": "postgres",
                "password": "1111",
                "host": "127.0.0.1",
                "port": "5432",
                "database": "postgres"
            }
            insert_weather_data(weather_data, connection_params)

    except KeyboardInterrupt:
        pass
    finally:
        c.close()

if __name__ == "__main__":
    run_consumer()