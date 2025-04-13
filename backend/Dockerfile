FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        linux-headers \
        postgresql-dev && \
    apk add --no-cache \
        libpq \
        postgresql-client 

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# RUN apk del .build-deps # Optional cleanup

# Copy entrypoint script and make it executable
COPY ./entrypoint.sh /entrypoint.sh  
RUN chmod +x /entrypoint.sh          

# Copy project code (after entrypoint script)
COPY . .

EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]       