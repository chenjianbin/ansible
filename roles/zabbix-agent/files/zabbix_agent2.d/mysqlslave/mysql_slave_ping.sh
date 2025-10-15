#!/bin/bash

SOCKET="/data0/mysql/$1/mysql.sock"
MYSQL="mysql -u root -S $SOCKET"

OUTPUT=$($MYSQL -e "SHOW REPLICA STATUS\G" 2>/dev/null)
if [ -z "$OUTPUT" ]; then
    OUTPUT=$($MYSQL -e "SHOW SLAVE STATUS\G" 2>/dev/null)
fi

# 兼容老字段名 (Slave_IO_Running, Slave_SQL_Running) 和新字段名 (Replica_IO_Running, Replica_SQL_Running)
STATUS=$(echo "$OUTPUT" | grep -P '(Slave_IO_Running|Slave_SQL_Running|Replica_IO_Running|Replica_SQL_Running)' | grep 'Yes' | wc -l)

if [ "$STATUS" = "2" ]; then
    echo 1
else
    echo 0
fi
