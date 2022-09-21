#!/usr/bin/env python3
import dns.resolver
import redis
from urllib.parse import urlparse
import re
import json
HOST_FILE = '/etc/hosts'
HG_REDIS_KEY = 'NEW_HGA030_V1_ACCOUNT_INFO'

def get_domain(key):
    domain_list = []
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    hg_url = json.loads(r.get(key))['hg_url']
    for h in hg_url:
        domain = urlparse(h['url']).netloc
        #domain = re.match(r'.*?([\w\.-]+).*?', netloc).groups()[0]
        domain_list.append(domain)
    return domain_list


def get_address(domain):
    try:
        results = dns.resolver.query(domain, 'A')
        for result in results.response.answer:
            for i in result.items:
                if i.rdtype == 1:
                    return i.address
    except Exception as e:
        pass
    return None

def modify_hosts():
    host_del_list = []
    host_add_list = []
    domain_list = get_domain(HG_REDIS_KEY)
    with open(HOST_FILE, 'r+') as f:
        info = f.readlines()
        for domain in domain_list:
            address = get_address(domain)
            if address:
                host_add_list.append('{0}    {1}\n'.format(address, domain))
                for i in info:
                    if i.split():
                        if i.split()[-1] == domain:
                            host_del_list.append(i)
        for i in host_del_list:
            info.remove(i)

    with open(HOST_FILE, 'w+') as f:
        for i in host_add_list:
            info.append(i)
        f.writelines(info)

if __name__ == '__main__':
    modify_hosts()
