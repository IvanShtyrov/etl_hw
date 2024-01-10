from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Строка соединения с Redis
redis_conn_string = "redis://localhost:6379/0"
redis_client = redis.Redis.from_url(redis_conn_string)

@app.route('/redis/data', methods=['GET'])
def get_redis_data():
    keys = redis_client.keys()
    # Декодирование ключей
    data = {key.decode('utf-8'): redis_client.get(key).decode('utf-8') for key in keys}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
