# A lightweight container for our PDF Assistant
FROM --platform=linux/amd64 python:3.10-slim

# Set up our workspace
WORKDIR /app

# Install the essentials first
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Bring in our code
COPY . /app

# Fire up the assistant!
CMD ["python", "app/src/main.py"]