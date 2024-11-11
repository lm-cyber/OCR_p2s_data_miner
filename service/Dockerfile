# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the bot script to the container

# Install dependencies
RUN pip install python-telegram-bot

# Define environment variables
ENV BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
COPY main.py .

# Run the bot
CMD ["python3", "main.py"]
