# Добавление новой темы для данных о погоде
WEATHER_DATA_TOPIC = "weather-data-topic"

def get_collection_topic(collection_name):
    match collection_name:
        case "WeatherData":
            topic = WEATHER_DATA_TOPIC
        case _:
            topic = None
    return topic
