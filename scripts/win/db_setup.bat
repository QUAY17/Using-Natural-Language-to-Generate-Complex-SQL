@echo off

echo "Creating docker network and volume"
docker network create --driver=bridge bg_data_net
docker volume create bg_data_vol

echo "Building mysql image"
docker build -t bg_db db
echo "Building flyway image"
docker build -t bg_flyway db/migration

./scripts/win/db_start.bat
echo "Sleeping to let MySQL Start"
timeout /t 30
echo "Starting flyway"
docker run --rm --name bg_flyway --net bg_data_net bg_flyway migrate