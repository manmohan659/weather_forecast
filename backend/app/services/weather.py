import httpx # type: ignore
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json
import csv
import xml.etree.ElementTree as ET
from io import StringIO

WEATHER_API_KEY = "b4396ce9a2e64262a00220130252201"
WEATHER_API_URL = "http://api.weatherapi.com/v1"

async def fetch_current_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{WEATHER_API_URL}/current.json",
            params={
                "key": WEATHER_API_KEY,
                "q": f"{latitude},{longitude}",
                "aqi": "no"
            }
        )
        response.raise_for_status()
        return response.json()

def format_weather_data_csv(weather_data: List[Dict]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["timestamp", "temperature", "humidity", "precipitation"])
    writer.writeheader()
    writer.writerows(weather_data)
    return output.getvalue()

def format_weather_data_xml(weather_data: List[Dict]) -> str:
    root = ET.Element("weather_data")
    for entry in weather_data:
        record = ET.SubElement(root, "record")
        for key, value in entry.items():
            ET.SubElement(record, key).text = str(value)
    return ET.tostring(root, encoding='unicode', method='xml')