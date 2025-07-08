FROM python:3.11-alpine

WORKDIR /app

COPY main.py .
COPY version.txt .

# Install FastAPI CLI tool (installs uvicorn too)
RUN pip install fastapi-cli fastapi

ENTRYPOINT ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]

#test