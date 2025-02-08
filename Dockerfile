# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster as builder

# Set environment variables

# Set work directory
WORKDIR /mock_server

# Install system dependencies and Python dependencies
COPY ./mock_server/requirements.txt /mock_server/
RUN pip install -r requirements.txt

FROM python:3.9-slim-buster as runner

WORKDIR /mock_server

# Install system dependencies and Python dependencies

# Copy project
COPY mock_server/* /mock_server/

# Expose the port the app runs in
EXPOSE 9000

# Define the command to start the container
CMD ["uvicorn", "mock_server.app.main:app", "--port", "9000"]