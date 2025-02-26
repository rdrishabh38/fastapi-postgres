#!/bin/sh
set -e

echo "Starting Fluentd container..."
docker-compose up -d fluentd

echo "Waiting 5 seconds for Fluentd to become healthy..."
sleep 5

echo "Starting DB and App containers..."
docker-compose up -d db app
