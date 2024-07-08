from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_analysis_route_by_city(mocker):
    mocker.patch('app.services.weather_fetcher.get_weather_data', return_value='weather_data')
    mocker.patch('app.services.data_visualization.get_visualizations', return_value=('visualizations, stats'))
    response = client.get("/analysis/", params={
        "city_name": "TestCity",
        "start_date": "2024-07-01",
        "end_date": "2024-07-03"
    })

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_analysis_route_by_coords(mocker):
    mocker.patch('app.services.weather_fetcher.get_weather_data', return_value='weather_data')
    mocker.patch('app.services.data_visualization.get_visualizations', return_value=('visualizations, stats'))
    response = client.get("/analysis/", params={
        "latitude": "12.34",
        "longitude": "56.78",
        "start_date": "2024-07-01",
        "end_date": "2024-07-03"
    })

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_analysis_route_invalid_input(mocker):
    mocker.patch('app.services.weather_fetcher.get_weather_data', return_value='weather_data')
    mocker.patch('app.services.data_visualization.get_visualizations', return_value=('visualizations, stats'))
    response = client.get("/analysis/", params={
        "start_date": "2024-07-01",
        "end_date": "2024-07-03"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "invalid input."}
