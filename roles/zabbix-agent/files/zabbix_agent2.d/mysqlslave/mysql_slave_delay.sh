#!/bin/bash

SOCKET="/data0/mysql/$1/mysql.sock"
MYSQL="mysql -u root -S $SOCKET"

# 优先尝试 SHOW REPLICA STATUS
OUTPUT=$($MYSQL -e "SHOW REPLICA STATUS\G" 2>/dev/null)
if [ -z "$OUTPUT" ]; then
    OUTPUT=$($MYSQL -e "SHOW SLAVE STATUS\G" 2>/dev/null)
fi

# 提取延迟字段（高版本 Seconds_Behind_Source，低版本 Seconds_Behind_Master）
TIME=$(echo "$OUTPUT" | grep -P 'Seconds_Behind_(Master|Source)' | awk -F: '{print $2}' | sed 's/[[:space:]]//g')

# 如果值为 NULL 或空，设置为 1000
if [ -z "$TIME" ] || [ "$TIME" = "NULL" ]; then
    TIME=1000
fi

echo "$TIME"
