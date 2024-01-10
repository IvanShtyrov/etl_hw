from confluent_kafka import Producer
import requests
import json

# Настройка Kafka Producer
p = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def fetch_weather_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def send_to_kafka(topic, data):
    p.produce(topic, json.dumps(data).encode('utf-8'), callback=delivery_report)
    # Проверка состояния доставки
    p.poll(0)

if __name__ == "__main__":
    api_url = "http://api.openweathermap.org/data/2.5/weather?q=Kazan,RU&appid=7390f9b849cf7b3b98365121df105ccb"
    weather_data = fetch_weather_data(api_url)
    if weather_data:
        send_to_kafka('weather_data', weather_data)
    p.flush()  # Ожидание доставки всех сообщений