FROM mongo

COPY exported_data.json /docker-entrypoint-initdb.d/
COPY mongo-import.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/mongo-import.sh