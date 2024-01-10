from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Строка соединения с PostgreSQL
pg_conn_string = "dbname='postgres' user='postgres' host='localhost' password='1111' port='5432'"
pg_conn = psycopg2.connect(pg_conn_string)

@app.route('/postgres/data', methods=['GET'])
def get_postgres_data():
    cursor = pg_conn.cursor()
    cursor.execute("SELECT * FROM weather_data;")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
