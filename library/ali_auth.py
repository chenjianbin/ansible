#!/usr/bin/env python
# coding: utf8

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['custominterface'],
    'supported_by': 'tony chen'
}

DOCUMENTATION = '''
---
module: ali_auth

short_description: The module provide signature function of aliyun Restful api

version_added: "2.4"

description:
    - "The module provide signature function of aliyun Restful api"

options:
    service:
        description:
            - Aliyun service name, example oss or ecs
        required: true
    key_id:
        description:
            - Aliyun account's accesskeyid
        required: true
    secret_key:
        description:
            - Aliyun account's accesskeysecret
        required: true
    url:
        description:
            - Aliyun resource's url
        required: ture
    verb:
        description:
            - Http request mode
        required: true

extends_documentation_fragment:
    - aliyun

author:
    - jianbin chen (546391242@qq.com)
'''

EXAMPLES = '''
Example signature for oss api service
 - ali_auth:
    name: oss
    key_id: sdfsdfsd9sdfsd7
    secret_key: slis786sdf678sd97
    url: https://aliyun.com/xxx/xxx
    verb: GET
'''

RETURN = '''
authorization:
    description: http header Authorization
    type: str
date:
    description: Http header GMT date
    type:str
'''

from ansible.module_utils.basic import AnsibleModule
from email.utils import formatdate
import hmac
import base64
import hashlib
import platform
if platform.python_version().split('.')[0] == '3':
    from urllib.parse import urlparse as urlparse
else:
    from urlparse import urlparse as urlparse

class OssAuth(object):
    def __init__(self, module):
        self.module = module
        self.service = module.params['service']
        self.key_id = module.params['key_id']
        self.secret_key = module.params['secret_key']
        self.url = module.params['url']
        self.verb = module.params['verb']
        self.datetime = formatdate(None, usegmt=True)

    def sign(self):
        args = self.verb.upper() + '\n\n\n' + self.datetime + '\n/' + urlparse(self.url).netloc.split('.')[0] + urlparse(self.url).path
        h = hmac.new(self.secret_key, args, hashlib.sha1)
        signature = base64.b64encode(h.digest())
        authorization = self.service.upper() + ' ' + self.key_id + ':' + signature
        return authorization, self.datetime




def main():
    module_args = dict(
        service = dict(type='str', required=True),
        key_id = dict(type='str', required=True),
        secret_key = dict(type='str', required=True),
        url = dict(type='str', required=True),
        verb = dict(type='str', required=True)
    )
    result = dict(
        changed = False,
    )
    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True
    )

    if module.check_mode:
        return result

    if module.params['service'].upper() == 'OSS':
        result['authorization'], result['date'] = OssAuth(module).sign()
        result['changed'] = True
    else:
        module.fail_json(msg='Not service', **result)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
