#!/usr/bin/env python
import os
import json
import re
MYSQL_PATH = '/data0/mysql/'

def discover(path):
        ports = [ {'{#MYSQLPORT}':d} for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and re.match('^[1-5]?[0-9]{1,4}$', d) and d != "3306"]
        print(json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':')))

if __name__ == '__main__':
    discover(MYSQL_PATH)
