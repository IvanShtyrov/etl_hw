import unittest
from unittest.mock import patch, MagicMock
from app.mongo_insert import fetch_and_insert_weather_data

class TestMongoInsert(unittest.TestCase):

    @patch('app.mongo_insert.requests.get')
    @patch('app.mongo_insert.MongoClient')
    def test_fetch_and_insert_weather_data(self, mock_mongo_client, mock_requests_get):
        # Настроим мок для запроса к API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"weather": "sunny", "temperature": "23"}
        mock_requests_get.return_value = mock_response

        # Настроим мок для вставки данных в MongoDB
        mock_mongo_collection = MagicMock()
        mock_mongo_collection.insert_one.return_value.inserted_id = "test_id"
        mock_mongo_db = MagicMock()
        mock_mongo_db.__getitem__.return_value = mock_mongo_collection
        mock_mongo_client.return_value.__getitem__.return_value = mock_mongo_db

        # API URL и строка подключения к MongoDB
        api_url = 'http://fakeapi.com/weather'
        mongo_connection_string = 'mock_connection_string'
        db_name = 'WeatherData'
        collection_name = 'CurrentWeather'

        # Вызов тестируемой функции
        result = fetch_and_insert_weather_data(api_url, mongo_connection_string, db_name, collection_name)

        # Проверки
        mock_requests_get.assert_called_with(api_url)
        mock_mongo_collection.insert_one.assert_called_with({"weather": "sunny", "temperature": "23"})
        self.assertEqual(result, "test_id")

if __name__ == '__main__':
    unittest.main()
