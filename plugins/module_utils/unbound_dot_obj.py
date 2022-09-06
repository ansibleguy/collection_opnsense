import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    is_ip, valid_hostname
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session


class DnsOverTls:
    FIELD_ID = 'dot_name'
    CMDS = {
        'add': 'addForward',
        'del': 'delForward',
        'set': 'setForward',
        'search': 'get',
        'toggle': 'toggleForward',
    }
    API_KEY = 'dot'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.dot = {}
        self.call_cnf = {  # config shared by all calls
            'module': 'unbound',
            'controller': 'settings',
        }
        self.existing_dots = None

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
        if not validators.domain(self.p['domain']):
            self.m.fail_json(f"Value '{self.p['domain']}' is an invalid domain!")

        if not validators.between(int(self.p['port']), 1, 65535):
            self.m.fail_json(f"Value '{self.p['port']}' is an invalid port!")

        if self.p['verify'] not in ['', None] and \
                not is_ip(self.p['verify']) and \
                not valid_hostname(self.p['verify']):
            self.m.fail_json(f"Value '{self.p['verify']}' neither a valid IP-Address "
                             f"nor a valid hostname!")

        # checking if item exists
        self._find_dot()
        if self.exists:
            self.call_cnf['params'] = [self.dot['uuid']]

        self.r['diff']['after'] = self._build_diff_after()

    def _find_dot(self):
        if self.existing_dots is None:
            self.existing_dots = self.search_call()

        for existing in self.existing_dots:
            _matching = []
            existing = self._simplify_existing(existing)

            for field in ['domain', 'target']:
                _matching.append(existing[field] == self.p[field])

            if all(_matching):
                self.dot = existing
                self.r['diff']['before'] = self.dot
                self.exists = True
                break

    def search_call(self) -> list:
        dots = []
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']['dots'][self.API_KEY]

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if dot['type']['dot']['selected'] in [1, '1', True]:
                    dot.pop('type')
                    dot['uuid'] = uuid
                    dots.append(dot)

        return dots

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
        for field in ['domain', 'target', 'enabled', 'port', 'verify']:
            if str(self.dot[field]) != str(self.p[field]):
                self.r['changed'] = True
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

    @staticmethod
    def _simplify_existing(dot: dict) -> dict:
        # makes processing easier
        return {
            'uuid': dot['uuid'],
            'domain': dot['domain'],
            'target': dot['server'],
            'port': int(dot['port']),
            'verify': dot['verify'],
            'enabled': dot['enabled'] in [1, '1', True],
        }

    def _build_diff_after(self) -> dict:
        return {
            'uuid': self.dot['uuid'] if 'uuid' in self.dot else None,
            'domain': self.p['domain'],
            'target': self.p['target'],
            'port': self.p['port'],
            'verify': self.p['verify'],
            'enabled': self.p['enabled'],
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'type': 'dot',
                'enabled': 1 if self.p['enabled'] else 0,
                'domain': self.p['domain'],
                'server': self.p['target'],
                'verify': self.p['verify'],
                'port': self.p['port'],
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

    def reconfigure(self):
        # reload running config
        if not self.m.check_mode:
            self.s.post(cnf={
                'module': self.call_cnf['module'],
                'controller': 'service',
                'command': 'reconfigure',
                'params': []
            })
