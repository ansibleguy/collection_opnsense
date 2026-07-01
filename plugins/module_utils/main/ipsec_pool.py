from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Pool(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'pool'
    API_MOD = 'ipsec'
    API_CONT = 'pools'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['network', 'dns']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {'network': 'addrs'}
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['dns']
    }
    EXIST_ATTR = 'pool'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.pool = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['network']):
                self.m.fail_json("You need to provide a 'network' to create an IPSec-Pool!")

            for ip in self.p['dns']:
                if is_ip(ip):
                    continue
                self.m.fail_json(
                    f"It seems you provided an invalid IP address as dns: '{ip}'"
                )

        self._base_check()
