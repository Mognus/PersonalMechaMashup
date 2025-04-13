
# Use Python 3.11 Alpine runtime as a parent image
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies required for psycopg2 on Alpine
# and build dependencies that can be removed later
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        linux-headers \
        # psycopg2 dependencies
        postgresql-dev && \
    apk add --no-cache \
        # psycopg2 runtime dependencies (needed even after build)
        libpq

# Install Python dependencies from requirements.txt
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Remove build dependencies after installing Python packages (optional)
# RUN apk del .build-deps

# Copy project code into the container
COPY . .

# Expose the port the app runs on (though docker-compose handles the mapping)
EXPOSE 8000

# Command to run the application (will be overridden by docker-compose for dev)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]