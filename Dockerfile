# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY src/backend/ ./backend/
COPY src/frontend/ ./frontend/

COPY .env ./.env

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "backend/app.py"]