import requests
import dotenv
import os

dotenv.load_dotenv()


def fetch_weather(city):
    key = os.getenv('API_KEY')
    url = f'https://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no'
    response = requests.get(url)
    try:
        result = response.json()['current']['temp_c']
    except KeyError:
        result = None
    return result


print(fetch_weather('dfs'))