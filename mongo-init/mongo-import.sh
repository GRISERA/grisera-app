#!/bin/bash
set -e

mongo_host="localhost"
mongo_port="18181"

# Wait for MongoDB to be ready
until mongosh --host "$mongo_host" --port "$mongo_port" -u user -p password --authenticationDatabase=admin --eval "printjson(db.serverStatus())" > /dev/null 2>&1; do
    echo "MongoDB is not ready - waiting..."
    sleep 1
done

echo "MongoDB is ready - importing data..."

mongoimport --host=localhost --port=18181 -u user -p password --authenticationDatabase=admin --db=mydatabase --collection=users --type=json --file=/docker-entrypoint-initdb.d/exported_data.json --jsonArray
