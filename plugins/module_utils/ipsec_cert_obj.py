from hashlib import sha256 as hash_sha256

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    get_matching, get_simple_existing, get_selected


class KeyPair:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY = 'keyPair'
    API_MOD = 'ipsec'
    API_CONT = 'key_pairs'
    API_CONT_REL = 'legacy_subsystem'
    API_CMD_REL = 'applyConfig'
    CHANGE_CHECK_FIELDS = ['public_key']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.key = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_keys = None

    def process(self):
        if self.p['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if self.exists:
                self.update()

            else:
                self.create()

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
        self._find_key()
        if self.exists:
            self.call_cnf['params'] = [self.key['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self._build_diff(data=self.p)

    def _find_key(self):
        if self.existing_keys is None:
            self.existing_keys = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_keys,
            compare_item=self.p, match_fields=[self.FIELD_ID],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.key = match
            self.r['diff']['before'] = self._build_diff(data=self.key)
            self.exists = True

    def _error(self, msg: str):
        # for special handling of errors
        self.m.fail_json(msg)

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

    def _search_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['ipsec']['keyPairs'][self.API_KEY]

    def create(self):
        self.r['changed'] = True

        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['add'],
                    'data': self._build_request(),
                }
            })

    def update(self):
        # checking if changed
        for field in self.CHANGE_CHECK_FIELDS:
            if str(self.key[field]) != str(self.p[field]):
                self.r['changed'] = True
                # raise SystemExit(f"{field} - {self.key[field]} != {self.p[field]}")
                break

        # update if changed
        if self.r['changed']:
            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

            if not self.m.check_mode:
                self.s.post(cnf={
                    **self.call_cnf, **{
                        'command': self.CMDS['set'],
                        'data': self._build_request(),
                    }
                })

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

    @staticmethod
    def _build_diff(data: dict) -> dict:
        return {
            'type': data['type'],
            'public_key': data['public_key'],
            'name': data['name'],
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'keyType': self.p['type'],
                'publicKey': self.p['public_key'],
                'privateKey': self.p['private_key'],
                'name': self.p['name'],
            }
        }

    def delete(self):
        self.r['changed'] = True
        self.r['diff']['after'] = {}

        if not self.m.check_mode:
            self._delete_call()

            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': self.CMDS['del']}})

    def reload(self):
        # reload the running config
        if not self.m.check_mode:
            self.s.post(cnf={  # config shared by all calls
                'module': self.API_MOD,
                'controller': self.API_CONT_REL,
                'command': self.API_CMD_REL,
            })
