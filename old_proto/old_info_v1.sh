#!/bin/bash

start_time=`date +%s`

mysql -h{ip} -u{root} -p{passwd} -D{database} < sql/app_old_desc.sql --default-character-set=utf8 > sql/result.txt

python old_info.py

mysql -h{ip} -u{root} -p{passwd} -D{database}  < sql/app_old_info.sql --default-character-set=utf8 

end_time=`date +%s`

use_time_minutes=$((($(($end_time-$start_time))) / 60))
use_time_seconds=$((($(($end_time-$start_time))) % 60))

echo It takes $use_time_minutes minutes $use_time_seconds seconds
