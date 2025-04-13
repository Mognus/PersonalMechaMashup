#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Optional: Wait for Database ---
# Simple loop to wait for the database to be ready.
# Adjust DB_HOST, DB_PORT based on your docker-compose service name and port.
DB_HOST="db" # Service name from docker-compose.yml
DB_PORT="5432" # Default PostgreSQL port

# Check if 'pg_isready' command exists (part of postgresql-client)
# If not, this check will be skipped. Install 'postgresql-client' in Dockerfile if needed.
if command -v pg_isready > /dev/null; then
    echo "Waiting for database on ${DB_HOST}:${DB_PORT}..."
    # Loop until pg_isready returns success (0)
    # -h: host, -p: port, -U: user (optional, defaults often work) -q: quiet
    while ! pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -q; do
        # Print a dot to show progress, sleep for 1 second
        printf "."
        sleep 1
    done
    echo "\nDatabase is ready!"
else
    echo "WARNING: 'pg_isready' command not found. Skipping database readiness check."
    echo "Consider adding 'postgresql-client' (or 'postgresql-libs' on newer Alpine) to your Dockerfile's apk add command."
    # Fallback: Simple sleep for a few seconds (less reliable)
    # echo "Waiting for a few seconds assuming DB starts..."
    # sleep 5
fi
# --- End Optional: Wait for Database ---


# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Optional: Collect static files ( uncomment if you want static files collected on start)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput --clear

# Execute the main command (passed as arguments to this script)
# "$@" executes the command passed to the entrypoint (e.g., from docker-compose command)
echo "Starting server..."
exec "$@"