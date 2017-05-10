#!/bin/bash

start_time=`date +%s`

python new_info.py

mysql -h{ip} -u{root} -p{passwd} -D{database} < sql/app_new_info.sql --default-character-set=utf8 

end_time=`date +%s`

use_time_minutes=$((($(($end_time-$start_time))) / 60))
use_time_seconds=$((($(($end_time-$start_time))) % 60))

echo It takes $use_time_minutes minutes $use_time_seconds seconds
