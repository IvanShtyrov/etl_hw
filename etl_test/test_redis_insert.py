import unittest
import json
from unittest.mock import patch, MagicMock
from app.redis_insert import save_to_redis

class TestRedisInsert(unittest.TestCase):
    @patch('app.redis_insert.redis.Redis')
    def test_save_to_redis(self, mock_redis_class):
        # мок объекта Redis
        mock_redis_client = MagicMock()
        mock_redis_class.return_value = mock_redis_client

        # Тестовые данные и настройки
        test_data = {'temperature': 23, 'condition': 'Sunny'}
        test_key = 'weather_data'
        expire_time = 86400

        # Тестируемая функция
        save_to_redis(mock_redis_client, test_key, test_data, expire_time)

        # Проверяем, что метод setex был вызван с правильными аргументами
        mock_redis_client.setex.assert_called_with(test_key, expire_time, json.dumps(test_data))

if __name__ == '__main__':
    unittest.main()