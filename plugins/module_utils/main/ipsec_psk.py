from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class PreSharedKey(BaseModule):
    FIELD_ID = 'identity_local'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'searchItem',
        'detail': 'getItem',
    }

    API_KEY_PATH = 'preSharedKey'
    API_MOD = 'ipsec'
    API_CONT = 'pre_shared_keys'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['identity_remote', 'psk', 'type']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'identity_local': 'ident',
        'identity_remote': 'remote_ident',
        'psk': 'Key',
        'type': 'keyType',
    }
    FIELDS_TYPING = {
        'select': ['type'],
    }
    EXIST_ATTR = 'psk'
    TIMEOUT = 30.0  # ipsec reload
    FIELDS_DIFF_NO_LOG = ['psk']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.psk = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['psk']):
                self.m.fail_json('You need to supply a PSK!')

        self._base_check()

    def update(self) -> None:
        self.b.update(enable_switch=False)
