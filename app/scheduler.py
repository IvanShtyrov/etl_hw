import schedule
import time
from mongo_insert import fetch_and_insert_weather_data
from postgres_insert import process_messages
from redis_insert import insert_to_redis

# Настройки
api_url = 'http://api.openweathermap.org/data/2.5/weather?q=Kazan,RU&appid=7390f9b849cf7b3b98365121df105ccb'
mongo_connection_string = 'mongodb+srv://shtyrovin:test1111@cluster0.aagznte.mongodb.net/WeatherData?retryWrites=true&w=majority'
db_name = 'WeatherData'
collection_name = 'CurrentWeather'

# Функция для запуска обновления данных о погоде
def job_fetch_and_insert_weather_data():
    print("Обновление данных о погоде")
    fetch_and_insert_weather_data(api_url, mongo_connection_string, db_name, collection_name)

# Функция для запуска обработки сообщений Kafka
def job_process_messages():
    print("Обработка сообщений Kafka")
    process_messages()

# Запланировать выполнение задач
schedule.every(1).hours.do(job_fetch_and_insert_weather_data)
schedule.every(1).hours.do(job_process_messages)

# Бесконечный цикл для выполнения запланированных задач
while True:
    schedule.run_pending()
    time.sleep(1)