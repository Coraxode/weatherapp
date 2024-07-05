import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
API_URL = "https://api.weatherbit.io/v2.0/"
