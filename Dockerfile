# Use the official Python image from the Docker Hub
FROM python:3.10.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev libmariadb-dev

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . /app/

# Copy the .env file to the working directory
COPY .env /app/.env

# Expose port 8000 for the ASGI server
EXPOSE 8000

# Command to run the Daphne server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "yourproject.asgi:application"]

