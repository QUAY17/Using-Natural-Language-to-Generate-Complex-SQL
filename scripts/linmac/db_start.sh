#!/bin/bash
set -e

docker run --rm --net bg_data_net --name bg_db -p 127.0.0.1:3306:3306 --mount type=volume,source=bg_data_vol,destination=/var/lib/mysql -d bg_db