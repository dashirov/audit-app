# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY src/backend_v2/requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY  src/backend_v2/models    models
COPY  src/backend_v2/routes    routes
COPY  src/backend_v2/app.py    .
COPY  src/backend_v2/config.py    .
COPY  src/backend_v2/.env .

RUN apt-get update && apt-get install -y tree
RUN tree -a /app
# Expose port
EXPOSE 5172

# Run app
CMD ["python", "/app/app.py"]