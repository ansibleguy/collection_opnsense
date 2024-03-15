from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_selected, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class PreSharedKey(BaseModule):
    FIELD_ID = 'ident'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }

    API_KEY_PATH = 'ipsec.preSharedKeys.preSharedKey'
    API_MOD = 'ipsec'
    API_CONT = 'pre_shared_keys'
    API_CONT_REL = 'legacy_subsystem'
    API_CMD_REL = 'applyConfig'
    FIELDS_STRING = ['ident', 'remote_ident', 'psk']
    FIELDS_ALL = FIELDS_STRING + ['type']
    FIELDS_CHANGE = FIELDS_ALL
    FIELDS_TRANSLATE = {
        'ident': 'ident',
        'remote_ident': 'remote_ident',
        'psk': 'Key',
        'type': 'keyType',
    }
    FIELDS_TYPING = {}
    FIELDS_DIFF_EXCLUDE = []
    EXIST_ATTR = 'psk'
    TIMEOUT = 30.0  # ipsec reload

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.psk = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            for field in self.FIELDS_ALL:
                if is_unset(self.p[field]):
                    self.m.fail_json(
                        "You need to supply '{}' to create an IPSec certificate!".format(field)
                    )
                self.p[field] = self.p[field].strip()
        self._base_check()

    def _simplify_existing(self, psk: dict) -> dict:
        self.m.warn(f'current psk: {psk}')
        # makes processing easier
        simple = {}
        for field in self.FIELDS_STRING:
            for k, v in self.FIELDS_TRANSLATE.items():
                if field == k:
                    simple[k] = psk[v]
        simple['type'] = get_selected(psk['keyType'])

        if 'uuid' in psk:
            simple['uuid'] = psk['uuid']

        elif self.key is not None and 'uuid' in self.key:
            simple['uuid'] = self.key['uuid']

        else:
            simple['uuid'] = None

        self.m.warn(f'simple: {simple}')
        return simple

    def update(self) -> None:
        self.b.update(enable_switch=False)
        return
