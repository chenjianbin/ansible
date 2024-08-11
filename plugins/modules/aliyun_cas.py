# -*- coding: utf-8 -*-
# Copyright: (c) 2024, tony chen <keep0tony@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: aliyun_cas

short_description: The module provide certificate management function of aliyun

version_added: "2.4"

description:
    - "The module provide certificate management function of aliyun"

options:
    name:
        description:
            - Certificate name
        required: true
    cert:
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
    - tony chen (keep0tony@gmail.com)
'''

EXAMPLES = '''
Example signature for oss api service
 - aliyun_sign:
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

class Sign(object):
    def __init__(self, module):
        self.module = module
        self.service = module.params['service']
        self.key_id = module.params['key_id']
        self.secret_key = module.params['secret_key']
        self.url = module.params['url']
        self.verb = module.params['verb']
        self.datetime = formatdate(None, usegmt=True)

    def __call__(self):
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

    try:
        result['authorization'], result['date'] = Sign(module)()
        result['changed'] = True
    except:
        module.fail_json(msg='Signature failed!', **result)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
