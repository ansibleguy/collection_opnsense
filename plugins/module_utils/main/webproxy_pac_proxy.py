from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset


class Proxy(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addPACProxy',
        'set': 'setPACProxy',
        'del': 'delPACProxy',
        'search': 'get',
    }
    API_KEY_PATH = 'proxy.pac.proxy'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['type', 'url', 'description']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'type': 'proxy_type',
    }
    FIELDS_TYPING = {
        'select': ['type'],
    }
    EXIST_ATTR = 'proxy'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.proxy = {}

    def check(self):
        if self.p['state'] == 'present':
            if is_unset(self.p['url']):
                self.m.fail_json('You need to provide an URL to create a PAC-proxy!')

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.proxy['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)
