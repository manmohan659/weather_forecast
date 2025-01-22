from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.models.weather import (
    LocationCreate, Location, WeatherDataCreate, 
    WeatherData, WeatherResponse, DateRangeParams
)
from app.services.weather import (
    fetch_current_weather, format_weather_data_csv,
    format_weather_data_xml
)
from app.core import supabase 

router = APIRouter()

@router.post("/locations/", response_model=Location)
async def create_location(location: LocationCreate):
    try:
        # Validate location exists by fetching weather
        weather = await fetch_current_weather(location.latitude, location.longitude)
        
        result = supabase.table("locations").insert({
            "name": location.name,
            "latitude": location.latitude,
            "longitude": location.longitude
        }).execute()
        
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/locations/", response_model=List[Location])
async def get_locations():
    result = supabase.table("locations").select("*").execute()
    return result.data

@router.post("/weather/", response_model=WeatherData)
async def create_weather_data(weather_data: WeatherDataCreate):
    try:
        result = supabase.table("weather_data").insert({
            "location_id": str(weather_data.location_id),
            "temperature": weather_data.temperature,
            "humidity": weather_data.humidity,
            "precipitation": weather_data.precipitation,
            "timestamp": weather_data.timestamp.isoformat()
        }).execute()
        
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/weather/{location_id}", response_model=List[WeatherData])
async def get_weather_data(
    location_id: UUID,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = supabase.table("weather_data").select("*").eq("location_id", str(location_id))
    
    if start_date:
        query = query.gte("timestamp", start_date.isoformat())
    if end_date:
        query = query.lte("timestamp", end_date.isoformat())
    
    result = query.execute()
    return result.data

@router.put("/weather/{weather_id}", response_model=WeatherData)
async def update_weather_data(weather_id: UUID, weather_data: WeatherDataCreate):
    try:
        result = supabase.table("weather_data").update({
            "temperature": weather_data.temperature,
            "humidity": weather_data.humidity,
            "precipitation": weather_data.precipitation,
            "timestamp": weather_data.timestamp.isoformat()
        }).eq("id", str(weather_id)).execute()
        
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/weather/{weather_id}")
async def delete_weather_data(weather_id: UUID):
    try:
        supabase.table("weather_data").delete().eq("id", str(weather_id)).execute()
        return {"message": "Weather data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/export/weather/{location_id}")
async def export_weather_data(
    location_id: UUID,
    format: str = Query(..., regex="^(json|csv|xml)$"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    weather_data = await get_weather_data(location_id, start_date, end_date)
    
    if format == "json":
        return weather_data
    elif format == "csv":
        return format_weather_data_csv(weather_data)
    elif format == "xml":
        return format_weather_data_xml(weather_data)