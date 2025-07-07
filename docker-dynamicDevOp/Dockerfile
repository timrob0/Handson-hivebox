FROM alpine:3.19

# Install python3 and bash (optional, if you want bash)
RUN apk add --no-cache python3

WORKDIR /app

COPY main.py .
COPY version.txt .

RUN chmod +x main.py

ENTRYPOINT ["./main.py"]
