#!/bin/sh

# Wait for Kibana to be ready (adjust timeout as needed)
until curl -s -f -o /dev/null http://kibana:5601/api/status; do
  echo "Waiting for Kibana..."
  sleep 5
done

# Create the data view via Kibana API
curl -X POST "http://kibana:5601/api/data_views/data_view" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d @/kibana-data-view.json
