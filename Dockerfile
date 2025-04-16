# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y git nats-server

# Set up virtual environment and install Python dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Expose port 5000 for the dashboard server
EXPOSE 5000

# Run the deployment script when the container launches
CMD [ "bash", "-c", "source venv/bin/activate && python3 scripts/deploy_agents.py" ]
