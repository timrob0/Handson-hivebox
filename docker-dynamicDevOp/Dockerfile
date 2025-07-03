# Use a lightweight base image for our application
FROM alpine:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the 'hello.sh' script from your local machine to the /app directory in the container
COPY hello.sh .

# Copy the 'version.txt' file from your local machine to the /app directory in the container
COPY version.txt .

# Make the 'hello.sh' script executable
RUN chmod +x hello.sh

# Set the command that runs when the container starts
ENTRYPOINT ["./hello.sh"]
