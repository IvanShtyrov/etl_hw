import requests
import json
import redis
from app.decorators import logger

def fetch_weather_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code}")

@logger
def create_redis_client(host, port, db):
    return redis.Redis(host=host, port=port, db=db)

@logger
def save_to_redis(redis_client, key, data, expire_time):
    redis_client.setex(key, expire_time, json.dumps(data))

if __name__ == "__main__":
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q=Kazan,RU&appid=7390f9b849cf7b3b98365121df105ccb'

    redis_client = create_redis_client('127.0.0.1', 6379, 0)

    try:
        response = redis_client.ping()
        if response is True:
            print('Connected to Redis')
    except redis.exceptions.ConnectionError as e:
        print(f'Connection failed: {e}')
        exit(1)

    weather_data = fetch_weather_data(api_url)
    save_to_redis(redis_client, 'weather_data', weather_data, 86400)

    saved_data = redis_client.get('weather_data')
    if saved_data:
        print("Weather data saved to Redis:", saved_data.decode('utf-8'))
