#!/bin/bash
export PATH=/usr/local/webserver/mysql/bin:$PATH
TIME=`mysql -u root -S /data0/mysql/$1/mysql.sock -e "show slave status\G" 2> /dev/null|grep -P 'Seconds_Behind_Master'|awk -F\: '{print $2}'|sed s/[[:space:]]//g`
if [ $TIME == 'NULL' ]
then 
    TIME=1000
fi
echo $TIME
