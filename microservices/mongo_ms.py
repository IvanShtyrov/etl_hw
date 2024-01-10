from flask import Flask, Response
from pymongo import MongoClient
import json
from bson import ObjectId

app = Flask(__name__)

mongo_conn_string = "mongodb+srv://shtyrovin:test1111@cluster0.aagznte.mongodb.net/WeatherData?retryWrites=true&w=majority"
mongo_client = MongoClient(mongo_conn_string)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super(JSONEncoder, self).default(o)

# Устанавливаем наш JSONEncoder как стандартный для json.dumps
json.JSONEncoder.default = JSONEncoder().default

@app.route('/mongo/data', methods=['GET'])
def get_mongo_data():
    mongo_db = mongo_client['WeatherData']
    mongo_weather_data = mongo_db['CurrentWeather']
    data = list(mongo_weather_data.find({}))
    # Используем json.dumps для сериализации данных
    response = app.response_class(
        response=json.dumps(data, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
