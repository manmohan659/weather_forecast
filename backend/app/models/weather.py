from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional, List

class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

class WeatherDataBase(BaseModel):
    temperature: float
    humidity: float
    precipitation: float
    timestamp: datetime

class WeatherDataCreate(WeatherDataBase):
    location_id: UUID4

class WeatherData(WeatherDataBase):
    id: UUID4
    location_id: UUID4
    created_at: datetime
    updated_at: datetime

class WeatherResponse(BaseModel):
    location: Location
    weather_data: List[WeatherData]

class DateRangeParams(BaseModel):
    start_date: datetime
    end_date: datetime