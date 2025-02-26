#!/bin/sh
set -e

echo "Starting Fluentd container..."
docker compose up -d fluentd

echo "Waiting 5 seconds for Fluentd to become healthy..."
sleep 5

echo "Starting Elasticsearch container..."
docker compose up -d elasticsearch

echo "Waiting for Elasticsearch to become healthy..."
# Loop until Elasticsearch responds (adjust the URL/timeout as needed)
while ! curl -s http://localhost:9200 >/dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

echo "Starting Kibana container..."
docker compose up -d kibana

echo "Waiting 5 seconds for Kibana..."
sleep 5

echo "Starting DB and App containers..."
docker compose up -d db app
