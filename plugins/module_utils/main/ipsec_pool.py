from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


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
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['network']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {'network': 'addrs'}
    FIELDS_TYPING = {'bool': ['enabled']}
    EXIST_ATTR = 'pool'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.pool = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['network']):
                self.m.fail_json(
                    "You need to provide a 'network' to create an IPSec-Pool!"
                )

        self._base_check()
