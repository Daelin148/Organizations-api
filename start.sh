#!/bin/sh
set -e

echo "Cleaning up .gitkeep files..."
find ./postgres_data -name ".gitkeep" -type f -delete 2>/dev/null || true
echo "Cleanup completed"

docker compose -f 'docker-compose.yml' up -d --build