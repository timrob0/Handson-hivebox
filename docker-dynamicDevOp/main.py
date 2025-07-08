#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime, timedelta, timezone



app = FastAPI()

@app.get("/version")
def get_app_version() -> str:
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Unknown Version"
def read_version():
    return {"version": get_app_version()}

@app.get("/temperature")
def average_temperature():
    box_ids = [
        "5ade1acf223bd80019a1011c",
        "5c21ff8f919bf8001adf2488",
        "5ade1acf223bd80019a1011c"
    ]

    temperatures = []
    now = datetime.now(timezone.utc)

    for box_id in box_ids:
        try:
            response = requests.get(f"https://api.opensensemap.org/boxes/{box_id}", timeout=10)
            response.raise_for_status()
            box = response.json()

            for sensor in box.get("sensors", []):
                if "temperatur" in sensor.get("title", "").lower():
                    last = sensor.get("lastMeasurement")
                    if last:
                        timestamp = datetime.fromisoformat(last["createdAt"].replace("Z", "+00:00"))
                        if now - timestamp <= timedelta(hours=1):
                            value = float(last["value"])
                            temperatures.append(value)
                    break  # stop once we find the first valid temperature sensor

        except:
            continue  # skip any box that fails

    if not temperatures:
        raise HTTPException(status_code=404, detail="No recent temperature data found")

    avg_temp = sum(temperatures) / len(temperatures)
    return {
        "average_temperature": round(avg_temp, 2),
        "unit": "°C",
        "sources_counted": len(temperatures)
    }

def main():
    version = get_app_version()
    print(f"Version: {version}")

if __name__ == "__main__":
    main()
