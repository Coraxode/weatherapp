import requests
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.config import API_KEY, API_URL
from app.schemes import Location, LocationType


def get_date(date: str, difference: int) -> datetime:
    date = datetime.strptime(date, "%Y-%m-%d")

    if difference < 28:
        return date.strftime("%d")
    elif difference < 365:
        return date.strftime("%d-%m")
    else:
        return date.strftime("%d-%m-%Y")


def get_weather_data(
    location: Location,
    start_date: str,
    end_date: str,
) -> dict:
    api_url = API_URL
    api_key = API_KEY
    params = {"key": api_key}

    # Add info about location to parameters
    if location.type == LocationType.by_city:
        params['city'] = location.city_name
    elif location.type == LocationType.by_coords:
        params['lat'] = location.latitude
        params['lon'] = location.longitude

    # Add info about start_date and end_date (if needed).
    # Raise exception if only one of two is specified
    if start_date and end_date:
        # Add 1 day to the end date to receive the correct data via the API
        end_date = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        api_url += 'history/daily'
        params['start_date'] = start_date
        params['end_date'] = end_date

    try:
        response = requests.get(api_url, params=params).json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Raise exception if location info or response info is invalid
    if 'error' in response:
        raise HTTPException(status_code=400, detail=response['error'])
    if 'city_name' not in response:
        raise HTTPException(status_code=400, detail="Invalid location or date.")
    if response['data'][0]['temp'] is None:
        raise HTTPException(status_code=400, detail="Invalid request.")

    return proccess_weather_data(response)


def proccess_weather_data(weather_data: dict) -> dict:
    try:
        num_of_records = len(weather_data['data'])
        return_data = {"city": weather_data['city_name'], "num_of_records": num_of_records}
        return_data['data'] = []

        for weather in weather_data['data']:
            return_data['data'].append({
                "date": get_date(weather['datetime'], int(num_of_records)),
                "avg_temperature": weather['temp'],
                "avg_humidity": weather['rh'],
                "avg_wind_speed": weather['wind_spd'],
                "max_uv_index": weather['max_uv'],
            })
    except KeyError as err:
        raise HTTPException(status_code=400, detail=f"Missing key in weather data: {err}")
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"An error occurred: {err}")

    return return_data
