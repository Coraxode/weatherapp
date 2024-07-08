import json
from requests.models import Response
from fastapi.testclient import TestClient
from app.main import app
from app.schemes import Location, LocationType
from app.services.weather_fetcher import get_weather_data

client = TestClient(app)


def get_location_data():
    return Location(
        type=LocationType.by_city,
        city_name='Lviv'
    )


def get_request_data():
    data = {
        "city_id": "702550",
        "city_name": "Lviv",
        "country_code": "UA",
        "data": [
            {
                "clouds": 84,
                "datetime": "2024-07-03",
                "dewpt": 12.6,
                "dhi": 59,
                "dni": 477,
                "ghi": 352,
                "max_dhi": 118,
                "max_dni": 906,
                "max_ghi": 914,
                "max_temp": 19,
                "max_temp_ts": 1720011600,
                "max_uv": 3.2,
                "max_wind_dir": 320,
                "max_wind_spd": 1.8,
                "max_wind_spd_ts": 1720008000,
                "min_temp": 12.9,
                "min_temp_ts": 1719972000,
                "precip": 20,
                "precip_gpm": 20,
                "pres": 970,
                "revision_status": "interim",
                "rh": 83,
                "slp": 1007,
                "snow": 0,
                "snow_depth": None,
                "solar_rad": 154,
                "t_dhi": 1412,
                "t_dni": 11446,
                "t_ghi": 8440,
                "t_solar_rad": 3694,
                "temp": 15.7,
                "ts": 1719954000,
                "wind_dir": 320,
                "wind_gust_spd": 4,
                "wind_spd": 1.2
            }
        ],
        "lat": 49.83826,
        "lon": 24.02324,
        "sources": [
            "333930-99999",
            "UPM00033393",
            "imerg",
            "era5",
            "modis",
            "snodas"
        ],
        "state_code": "15",
        "station_id": "333930-99999",
        "timezone": "Europe/Kiev"
    }

    response = Response()
    response.status_code = 200
    response._content = json.dumps(data).encode('utf-8')
    response.headers['Content-Type'] = 'application/json'

    return response


def test_get_weather_data(mocker):
    request_data = get_request_data()
    mocker.patch('requests.get', return_value=request_data)
    location = get_location_data()

    weather_data = get_weather_data(location, '2024-07-01', '2024-07-03')

    assert weather_data['city'] == location.city_name
    assert weather_data['data'][0]['date'] == '03'
    assert weather_data['data'][0]['avg_temperature'] == request_data.json()['data'][0]['temp']
    assert weather_data['data'][0]['avg_humidity'] == request_data.json()['data'][0]['rh']
    assert weather_data['data'][0]['avg_wind_speed'] == request_data.json()['data'][0]['wind_spd']
    assert weather_data['data'][0]['max_uv_index'] == request_data.json()['data'][0]['max_uv']
