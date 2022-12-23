from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class KeyPair(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY = 'keyPair'
    API_KEY_1 = 'ipsec'
    API_KEY_2 = 'keyPairs'
    API_MOD = 'ipsec'
    API_CONT = 'key_pairs'
    API_CONT_REL = 'legacy_subsystem'
    API_CMD_REL = 'applyConfig'
    FIELDS_CHANGE = ['public_key']
    FIELDS_ALL = ['name', 'private_key', 'type']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'type': 'keyType',
        'public_key': 'publicKey',
        'private_key': 'privateKey',
    }
    FIELDS_DIFF_EXCLUDE = ['private_key']
    EXIST_ATTR = 'key'
    TIMEOUT = 30.0  # ipsec reload

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.s = Session(
            module=module,
            timeout=self.TIMEOUT,
        ) if session is None else session
        self.key = {}
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        if self.p['state'] == 'present':
            if self.p['public_key'] is None or self.p['private_key'] is None:
                self.m.fail_json(
                    "You need to supply both 'public_key' and "
                    "'private_key' to create an IPSec certificate!"
                )

            pub_start, pub_end = '-----BEGIN PUBLIC KEY-----', '-----END PUBLIC KEY-----'
            if self.p['public_key'].find(pub_start) == -1 or \
                    self.p['public_key'].find(pub_end) == -1:
                self.m.fail_json("The provided 'public_key' has an invalid format!")

            priv_start, priv_end = '-----BEGIN RSA PRIVATE KEY-----', '-----END RSA PRIVATE KEY-----'
            if self.p['private_key'].find(priv_start) == -1 or self.p['private_key'].find(priv_end) == -1:
                self.m.fail_json(
                    "The provided 'private_key' has an invalid format - should be "
                    "'RSA PRIVATE KEY'!"
                )

            self.p['public_key'] = self.p['public_key'].strip()
            self.p['private_key'] = self.p['private_key'].strip()

        # checking if item exists
        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.key['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _simplify_existing(self, key: dict) -> dict:
        # makes processing easier
        simple = {
            'type': get_selected(key['keyType']),
            'public_key': key['publicKey'].strip(),
            'private_key': key['privateKey'].strip(),
            'name': key['name'],
        }

        if 'uuid' in key:
            simple['uuid'] = key['uuid']

        elif self.key is not None and 'uuid' in self.key:
            simple['uuid'] = self.key['uuid']

        else:
            simple['uuid'] = None

        return simple

    def update(self):
        self.b.update(enable_switch=False)
