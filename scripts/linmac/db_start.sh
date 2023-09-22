#!/bin/bash
set -e

docker run --net bg_data_net --name bg_db -p 3306:3306 --mount type=volume,source=bg_data_vol,destination=/var/lib/mysql -d bg_db