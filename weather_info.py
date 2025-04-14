import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("OPEN_WEATHER_API_KEY is not set in .env file")
print("API KEY:", API_KEY)
city = "Chennai"
units = "metric"

params = {
    "q": city,
    "appid": API_KEY,
    "units": units # use "imperial" for Fahrenheit
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"Weather in {city}:")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Weather: {data['weather'][0]['description']}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
