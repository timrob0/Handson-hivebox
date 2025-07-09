"""
test_main.py
This module contains tests for the FastAPI application defined in main.py.
It includes tests for:
- Retrieving the application version.
- Extracting recent temperature data from sensors.
- Calculating the average temperature from multiple sensors.
"""
import os
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
import pytest
import requests
from main import app, extract_recent_temperature
# Create a test client for the FastAPI app

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_version_file():
    ''' Remove version.txt after each test if it exists
    If it exists, it will be removed to ensure a clean state for each test. 
    '''
    yield
    if os.path.exists("version.txt"):
        os.remove("version.txt")

def test_get_app_version_file_exists():
    ''' Test retrieving the application version from version.txt
    This test checks if the version is correctly read from the file.'''
    with open("version.txt", "w", encoding="utf-8") as f:
        f.write("1.2.3")
    response = client.get("/version")
    assert response.status_code == 200
    assert response.text.strip('"') == "1.2.3"

def test_get_app_version_file_missing():
    ''' Test retrieving the application version when version.txt is missing
    This test checks if the default "Unknown Version" is returned when the file does not exist'''
    if os.path.exists("version.txt"):
        os.remove("version.txt")
    response = client.get("/version")
    assert response.status_code == 200
    assert response.text.strip('"') == "Unknown Version"

def test_extract_recent_temperature_within_hour():
    ''' Test extracting recent temperature data from a sensor
    This test checks if the function correctly extracts the temperature value'''
    now = datetime.now(timezone.utc)
    sensor = {
        "title": "Temperatur",
        "lastMeasurement": {
            "createdAt": (now - timedelta(minutes=30)).isoformat().replace("+00:00", "Z"),
            "value": "22.5"
        }
    }
    assert extract_recent_temperature(sensor, now) == 22.5

def test_extract_recent_temperature_outside_hour():
    ''' Test extracting temperature data from a sensor that is outside the last hour
    This test checks if the function returns None for measurements older than one hour.'''
    now = datetime.now(timezone.utc)
    sensor = {
        "title": "Temperatur",
        "lastMeasurement": {
            "createdAt": (now - timedelta(hours=2)).isoformat().replace("+00:00", "Z"),
            "value": "18.0"
        }
    }
    assert extract_recent_temperature(sensor, now) is None

def test_extract_recent_temperature_wrong_title():
    ''' Test extracting temperature data from a sensor with a wrong title
    This test checks if the function returns None for sensors that do not have "Temperatur"'''
    now = datetime.now(timezone.utc)
    sensor = {
        "title": "Humidity",
        "lastMeasurement": {
            "createdAt": now.isoformat().replace("+00:00", "Z"),
            "value": "55"
        }
    }
    assert extract_recent_temperature(sensor, now) is None

@patch("main.requests.get")
def test_average_temperature_success(mock_get):
    ''' Test calculating the average temperature from multiple sensors
    This test checks if the average temperature is calculated correctly from multiple boxes.'''
    now = datetime.now(timezone.utc)
    # Mock three boxes, each with a valid temperature sensor
    mock_get.side_effect = [
        MockResponse({
            "sensors": [{
                "title": "Temperatur",
                "lastMeasurement": {
                    "createdAt": now.isoformat().replace("+00:00", "Z"),
                    "value": "20.0"
                }
            }]
        }),
        MockResponse({
            "sensors": [{
                "title": "Temperatur",
                "lastMeasurement": {
                    "createdAt": now.isoformat().replace("+00:00", "Z"),
                    "value": "22.0"
                }
            }]
        }),
        MockResponse({
            "sensors": [{
                "title": "Temperatur",
                "lastMeasurement": {
                    "createdAt": now.isoformat().replace("+00:00", "Z"),
                    "value": "24.0"
                }
            }]
        }),
    ]
    response = client.get("/temperature")
    assert response.status_code == 200
    data = response.json()
    assert data["average_temperature"] == 22.0
    assert data["unit"] == "°C"
    assert data["sources_counted"] == 3

@patch("main.requests.get")
def test_average_temperature_no_recent_data(mock_get):
    ''' Test calculating the average temperature when no recent data is available
    This test checks if a 404 error is returned when no valid temperature data is found.'''
    old_time = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat().replace("+00:00", "Z")
    mock_get.return_value = MockResponse({
        "sensors": [{
            "title": "Temperatur",
            "lastMeasurement": {
                "createdAt": old_time,
                "value": "18.0"
            }
        }]
    })
    response = client.get("/temperature")
    assert response.status_code == 404
    assert response.json()["detail"] == "No recent temperature data found"

@patch("main.requests.get")
def test_average_temperature_partial_failures(mock_get):
    ''' Test calculating the average temperature with partial failures
    This test checks if the average temperature is calculated correctly when some boxes fail.'''
    now = datetime.now(timezone.utc)
    # First box fails, second and third succeed
    mock_get.side_effect = [
    requests.RequestException("Network error"),
        MockResponse({
            "sensors": [{
                "title": "Temperatur",
                "lastMeasurement": {
                    "createdAt": now.isoformat().replace("+00:00", "Z"),
                    "value": "21.0"
                }
            }]
        }),
        MockResponse({
            "sensors": [{
                "title": "Temperatur",
                "lastMeasurement": {
                    "createdAt": now.isoformat().replace("+00:00", "Z"),
                    "value": "23.0"
                }
            }]
        }),
    ]
    response = client.get("/temperature")
    assert response.status_code == 200
    data = response.json()
    assert data["average_temperature"] == 22.0
    assert data["sources_counted"] == 2

class MockResponse:
    ''' Mock class to simulate requests.Response for testing
    This class mimics the behavior of requests.Response for testing purposes.
    It allows us to define custom JSON data and status codes for the response.'''
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        ''' Returns the JSON data of the response
        This method returns the JSON data that was set during initialization.'''
        return self._json

    def raise_for_status(self):
        ''' Raises an HTTPError if the response status code is not 200
        This method checks the status code and raises an exception if it is not 200.'''
        if self.status_code != 200:
            raise requests.HTTPError("HTTP error")
