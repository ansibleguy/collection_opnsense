from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class PreSharedKey(BaseModule):
    FIELD_ID = 'identity_local'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'search_item',
        'detail': 'get_item',
    }

    API_KEY_PATH = 'preSharedKey'
    API_MOD = 'ipsec'
    API_CONT = 'pre_shared_keys'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['description', 'identity_remote', 'psk', 'type']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'description': 'description',
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.psk = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['psk']):
                self.m.fail_json('You need to supply a PSK!')

        self._base_check()

    def update(self) -> None:
        self._base_update(enable_switch=False)
