#!/usr/bin/env python3

from fastapi import FastAPI

def get_app_version() -> str:
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Unknown Version"


app = FastAPI()

@app.get("/version")
def read_version():
    return {"version": get_app_version()}


def main():
    version = get_app_version()
    print(f"Version: {version}")

if __name__ == "__main__":
    main()
