from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.weather_fetcher import get_weather_data
from app.services.data_visualization import get_visualizations
from app.schemes import Location, LocationType as type
from typing import Optional

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")


@app.get("/analysis/")
def analysis(
    request: Request,
    start_date: str,
    end_date: str,
    city_name: Optional[str] = None,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
):
    if city_name:
        location = Location(type=type.by_city, city_name=city_name)
    elif latitude and longitude:
        location = Location(type=type.by_coords, latitude=latitude, longitude=longitude)
    else:
        raise HTTPException(status_code=400, detail="invalid input.")

    weather_data = get_weather_data(location=location, start_date=start_date, end_date=end_date)
    visualizations, descriptive_stats = get_visualizations(
        weather_data['data'],
        weather_data['num_of_records'],
    )
    context = {
        "city": weather_data['city'],
        "visualizations": visualizations,
        "descriptive_stats": descriptive_stats,
    }

    return templates.TemplateResponse(
        request=request,
        name="analysis.html",
        context=context,
    )
