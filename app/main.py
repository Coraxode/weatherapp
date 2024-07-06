from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.weather_fetcher import get_weather_data
from app.schemes import Location, LocationType as type

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(request=request, name="base.html")


@app.get("/analysis/")
def analysis(
    request: Request,
    city_name: str,
    latitude: str,
    longitude: str,
    start_date: str,
    end_date: str,
):
    if city_name:
        location = Location(type=type.by_city, city_name=city_name)
    elif latitude and longitude:
        location = Location(type=type.by_coords, latitude=latitude, longitude=longitude)
    else:
        raise HTTPException(status_code=400, detail="invalid input.")

    context = {"weather_data": get_weather_data(location=location, start_date=start_date, end_date=end_date)}

    return templates.TemplateResponse(
        request=request,
        name="analysis.html",
        context=context,
    )
