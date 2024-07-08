from fastapi.testclient import TestClient
from app.main import app
from app.services.data_visualization import get_visualizations

client = TestClient(app)


def get_weather_data():
    return [
        {
            'date': '01',
            'avg_temperature': 29.9,
            'avg_humidity': 54,
            'avg_wind_speed': 3.7,
            'max_uv_index': 11.6,
        },
        {
            'date': '02',
            'avg_temperature': 29.7,
            'avg_humidity': 53,
            'avg_wind_speed': 3.1,
            'max_uv_index': 11.6,
        },
        {
            'date': '03',
            'avg_temperature': 30.8,
            'avg_humidity': 40,
            'avg_wind_speed': 2.5,
            'max_uv_index': 11.6,
        },
    ]


def get_html_data():
    return """
    <table class="dataframe table">
    <thead>
        <tr style="text-align: right;">
        <th></th>
        <th>Temperature (°C)</th>
        <th>Humidity (%)</th>
        <th>Wind Speed (m/s)</th>
        <th>UV Index</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>Avg value</th>
        <td>30.13</td>
        <td>49.00</td>
        <td>3.1</td>
        <td>11.6</td>
        </tr>
        <tr>
        <th>Standard Deviation</th>
        <td>0.59</td>
        <td>7.81</td>
        <td>0.6</td>
        <td>0.0</td>
        </tr>
        <tr>
        <th>Min value</th>
        <td>29.70</td>
        <td>40.00</td>
        <td>2.5</td>
        <td>11.6</td>
        </tr>
        <tr>
        <th>25th Percentile</th>
        <td>29.80</td>
        <td>46.50</td>
        <td>2.8</td>
        <td>11.6</td>
        </tr>
        <tr>
        <th>50th Percentile</th>
        <td>29.90</td>
        <td>53.00</td>
        <td>3.1</td>
        <td>11.6</td>
        </tr>
        <tr>
        <th>75th Percentile</th>
        <td>30.35</td>
        <td>53.50</td>
        <td>3.4</td>
        <td>11.6</td>
        </tr>
        <tr>
        <th>Max value</th>
        <td>30.80</td>
        <td>54.00</td>
        <td>3.7</td>
        <td>11.6</td>
        </tr>
    </tbody>
    </table>
    """


def test_get_visualization_stats_table():
    weather_data = get_weather_data()
    visualizations, descriptive_stats = get_visualizations(weather_data, len(weather_data))

    assert '<table class="dataframe table">' in descriptive_stats
    assert '<th>Standard Deviation</th>' in descriptive_stats
    assert '<th>75th Percentile</th>' in descriptive_stats
