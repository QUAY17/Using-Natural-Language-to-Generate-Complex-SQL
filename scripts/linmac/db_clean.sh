#!/bin/bash
set -e

# docker kill bg_db
docker network rm bg_data_net
docker volume rm bg_data_vol