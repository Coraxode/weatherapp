from pydantic import BaseModel
from typing import Optional
from enum import Enum


class LocationType(str, Enum):
    by_city = "by_city"
    by_coords = "by_coords"


class Location(BaseModel):
    type: LocationType
    city_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
