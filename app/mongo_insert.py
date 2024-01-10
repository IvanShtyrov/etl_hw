from pymongo import MongoClient
import requests
import json
import functools
import time

def logger(func):
    """Логирует время выполнения функции."""
    @functools.wraps(func)
    def wrapper_logger(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__!r} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper_logger

@logger
def fetch_and_insert_weather_data(api_url, mongo_connection_string, db_name, collection_name):
    #клиент MongoDB
    mongo_client = MongoClient(mongo_connection_string)
    mongo_db = mongo_client[db_name]
    mongo_collection = mongo_db[collection_name]

    # Запрос к API OpenWeatherMap
    response = requests.get(api_url)
    if response.status_code == 200:
        weather_data = response.json()

        # Вставка данных о погоде в MongoDB
        insert_result = mongo_collection.insert_one(weather_data)
        print(f"Data inserted into MongoDB with id: {insert_result.inserted_id}")
        return insert_result.inserted_id
    else:
        print(f"Failed to get weather data from API. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q=Kazan,RU&appid=7390f9b849cf7b3b98365121df105ccb'
    mongo_connection_string = 'mongodb+srv://shtyrovin:test1111@cluster0.aagznte.mongodb.net/WeatherData?retryWrites=true&w=majority'
    db_name = 'WeatherData'
    collection_name = 'CurrentWeather'

    # Вызов функции для получения и вставки данных
    inserted_id = fetch_and_insert_weather_data(api_url, mongo_connection_string, db_name, collection_name)
    print(f"Inserted document ID: {inserted_id}")
