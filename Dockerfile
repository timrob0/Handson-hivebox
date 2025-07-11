FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENTRYPOINT ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
