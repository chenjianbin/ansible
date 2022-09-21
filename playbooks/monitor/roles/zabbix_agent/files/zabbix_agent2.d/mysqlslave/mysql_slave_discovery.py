#!/usr/bin/env python
from pathlib import Path,PurePath
import json
import re
MYSQL_PATH = '/data0/mysql/'

def discover(path):
        ports = [ {'{#MYSQLPORT}':d.name} for d in Path(path).glob('*') if d.is_dir() and re.fullmatch('[1-5]?[0-9]{1,4}', d.name) ]
        print(json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':')))

if __name__ == '__main__':
    discover(MYSQL_PATH)
