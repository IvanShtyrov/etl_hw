import unittest
from unittest.mock import patch, MagicMock
from app.postgres_insert import insert_weather_data

class TestPostgresInsert(unittest.TestCase):

    @patch('app.postgres_insert.psycopg2.connect')
    def test_insert_weather_data(self, mock_connect):
        # Создаем "магический" объект connection и cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Тестовые данные и параметры подключения
        test_data = {'data': 'test_data'}
        connection_params = {
            "user": "postgres",
            "password": "1111",
            "host": "127.0.0.1",
            "port": "5432",
            "database": "postgres"
        }

        # Вызов функции вставки данных
        insert_weather_data(test_data, connection_params)

        # Проверка, что было выполнено подключение к базе данных
        mock_connect.assert_called_with(**connection_params)

        # Проверка, что cursor.execute был вызван с правильными аргументами
        mock_cursor.execute.assert_called()

        # Проверка, что был выполнен commit транзакции
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
