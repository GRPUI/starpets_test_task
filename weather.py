# импортируем библиотеки
import requests
import dotenv
import os
from datetime import datetime, timedelta

# загружаем переменные окружения
dotenv.load_dotenv()

temperatures = {}


# функция для получения погоды
def fetch_weather(city):
    key = os.getenv('API_KEY')
    if city in temperatures.keys():
        delta = datetime.now() - temperatures[city]["timedelta"]
        if delta < timedelta(minutes=10):
            return temperatures[city]["temperature"]

    url = f'https://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no'
    response = requests.get(url)
    try:
        result = response.json()['current']['temp_c']
        temperatures[city] = {
            "temperature": result,
            "timedelta": datetime.now()
        }
    except KeyError:
        result = None
    return result


print(fetch_weather('dfs'))