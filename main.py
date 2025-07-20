#!/usr/bin/env python3
"""
Main FastAPI application for Hivebox DevOps Hands-On Project.

This module provides a FastAPI application with endpoints to:
- Retrieve the application version from env.
- Calculate the average temperature from a set of OpenSenseMap

Endpoints:
- GET /version: Returns the application version as a string.
- GET /temperature: Returns the average temperature (in °C) from the configured OpenSenseMap boxes.

Author: [Your Name]
"""

from datetime import datetime, timedelta, timezone
import os
from fastapi import FastAPI, HTTPException, Response
import requests
from dotenv import load_dotenv
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

load_dotenv()

# Load environment variables
OPENSENSEMAP_API_URL = os.getenv("OPENSENSEMAP_API_URL", "https://api.opensensemap.org")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
VERSION_FILE = os.getenv("VERSION_FILE", "Unknown Version")
box_ids = os.getenv(
    "OPENSENSEMAP_BOX_IDS",
    "5eba5fbad46fb8001b799786,5c21ff8f919bf8001adf2488,5ade1acf223bd80019a1011c"
).split(",")

if not box_ids or box_ids == ["0", "0", "0"]:
    raise ValueError("No valid OpenSenseMap box IDs provided in environment variables.")

# Initialize FastAPI application
app = FastAPI()

@app.get("/version")
def get_app_version() -> str:
    """
    Reads the application version from the VERSION_FILE environment variable.

    Returns:
        str: The version string, or 'Unknown Version' if not set.
    """
    return os.getenv("VERSION_FILE", "Unknown Version")


def read_version():
    """
    Returns the application version in a dictionary format.

    Returns:
        dict: Dictionary containing the version.
    """
    return {"version": get_app_version()}


def extract_recent_temperature(sensor, now):
    """
    Extracts the temperature value from a sensor if the measurement is within the last hour.
    Returns the value as float or None.
    """
    if "temperatur" in sensor.get("title", "").lower():
        last = sensor.get("lastMeasurement")
        if last:
            timestamp = datetime.fromisoformat(last["createdAt"].replace("Z", "+00:00"))
            if now - timestamp <= timedelta(hours=1):
                return float(last["value"])
    return None


@app.get("/temperature")
def average_temperature():
    """
    Calculates the average temperature from a set of OpenSenseMap sensor boxes.

    Only considers temperature measurements from the last hour. If no recent data is found,
    returns a 404 error.

    Returns:
        dict: Dictionary containing the average temperature, unit, and number of sources counted.
    """

    temperatures = []
    now = datetime.now(timezone.utc)

    for box_id in box_ids:
        try:
            response = requests.get(
                f"{OPENSENSEMAP_API_URL}/boxes/{box_id}", timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            box = response.json()

            for sensor in box.get("sensors", []):
                temp = extract_recent_temperature(sensor, now)
                if temp is not None:
                    temperatures.append(temp)
                    break  # stop once we find the first valid temperature sensor

        except (requests.RequestException, ValueError, KeyError):
            continue  # skip any box that fails

    if not temperatures:
        raise HTTPException(status_code=404, detail="No recent temperature data found")


    avg_temp = sum(temperatures) / len(temperatures)
    if avg_temp < 10:
        status = "Too cold"
    elif 10 < avg_temp < 36:
        status = "Normal"
    else:
        status = "Too hot"

    return {
        "average_temperature": round(avg_temp, 2),
        "unit": "°C",
        "sources_counted": len(temperatures),
        "status": status,
    }


@app.get("/metrics")
def metrics():
    """
    Exposes Prometheus metrics.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def main():
    """
    Main function to run the FastAPI app and print the version.
    """
    version = get_app_version()
    print(f"Version: {version}")


if __name__ == "__main__":
    main()
