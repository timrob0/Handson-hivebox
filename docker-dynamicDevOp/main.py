#!/usr/bin/env python3

def get_app_version() -> str:
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Unknown Version"

def main():
    version = get_app_version()
    print(f"Version: {version}")

if __name__ == "__main__":
    main()
