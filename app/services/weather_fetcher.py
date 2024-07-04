import requests
from app.config import API_KEY, API_URL
from app.schemes import Location


def get_weather_info(
    location: Location,
    start_date: str = None,
    end_date: str = None
) -> dict:
    api_url = API_URL
    api_key = API_KEY
    params = {"key": api_key}

    if location.type == "by_city":
        params['city'] = location.city_name
    elif location.type == "by_coords":
        params['lat'] = location.latitude
        params['lon'] = location.longitude

    if start_date and end_date:
        api_url += 'history/daily'
        params['start_date'] = start_date
        params['end_date'] = end_date
    else:
        api_url += 'current'

    response = requests.get(api_url, params=params)
    return proccess_weather_data(response.json())


def proccess_weather_data(weather_data: dict):
    return_data = {"city": weather_data['city_name']}
    return_data['data'] = []

    for weather in weather_data['data']:
        return_data['data'].append({
            "date": weather['datetime'],
            "avg_temperature": weather['temp'],
            "max_temperature": weather['max_temp'],
            "min_temperature": weather['min_temp'],
            "avg_humidity": weather['rh'],
            "avg_wind_speed": weather['wind_spd'],
            "max_uv_index": weather['max_uv'],
        })

    print(return_data)
