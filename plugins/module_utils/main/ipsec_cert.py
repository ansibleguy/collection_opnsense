import re
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    get_selected
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class KeyPair(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'search_item',
        'detail': 'get_item',
    }
    API_KEY_PATH = 'keyPair'
    API_MOD = 'ipsec'
    API_CONT = 'key_pairs'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['public_key']
    FIELDS_ALL = ['name', 'private_key', 'type']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'type': 'keyType',
        'public_key': 'publicKey',
        'private_key': 'privateKey',
    }
    FIELDS_DIFF_NO_LOG = ['private_key']
    EXIST_ATTR = 'key'
    FIELDS_TYPING = {}
    TIMEOUT = 30.0  # ipsec reload

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.key = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['public_key']) or is_unset(self.p['private_key']):
                self.m.fail_json(
                    "You need to supply both 'public_key' and "
                    "'private_key' to create an IPSec certificate!"
                )

            pub_start, pub_end = '-----BEGIN PUBLIC KEY-----', '-----END PUBLIC KEY-----'
            if self.p['public_key'].find(pub_start) == -1 or \
                    self.p['public_key'].find(pub_end) == -1:
                self.m.fail_json("The provided 'public_key' has an invalid format!")

            priv_start, priv_end = '-----BEGIN (RSA | EC )?PRIVATE KEY-----', '-----END (RSA | EC )?PRIVATE KEY----- *$'
            if (
                re.match(priv_start, self.p['private_key']) is None or
                re.search(priv_end, self.p['private_key']) is None
            ):
                self.m.fail_json(
                    "The provided 'private_key' has an invalid format - should be "
                    f"'{self.p['type'].upper()} PRIVATE KEY'!"
                )

            self.p['public_key'] = self.p['public_key'].strip()
            self.p['private_key'] = self.p['private_key'].strip()

        self._base_check()

    def simplify_existing(self, key: dict) -> dict:
        # makes processing easier
        simple = {
            'type': get_selected(key['keyType']),
            'public_key': key.get('publicKey', '').strip(),
            'private_key': key.get('privateKey', '').strip(),
            'name': key['name'],
        }

        if 'uuid' in key:
            simple['uuid'] = key['uuid']

        elif self.key is not None and 'uuid' in self.key:
            simple['uuid'] = self.key['uuid']

        else:
            simple['uuid'] = None

        return simple

    def update(self) -> None:
        self._base_update(enable_switch=False)
