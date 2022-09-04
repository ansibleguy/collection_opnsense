import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session


class Forward:
    FIELD_ID = 'fwd_name'
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
        self.fwd = {}
        self.call_cnf = {  # config shared by all calls
            'module': 'unbound',
            'controller': 'settings',
        }
        self.existing_fwds = None

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

        # checking if item exists
        self._find_fwd()
        if self.exists:
            self.call_cnf['params'] = [self.fwd['uuid']]

        self.r['diff']['after'] = self._build_diff_after()

    def _find_fwd(self):
        if self.existing_fwds is None:
            self.existing_fwds = self.search_call()

        for existing in self.existing_fwds:
            _matching = []
            existing = self._simplify_existing(existing)

            for field in ['domain', 'target']:
                _matching.append(existing[field] == self.p[field])

            if all(_matching):
                self.fwd = existing
                self.r['diff']['before'] = self.fwd
                self.exists = True
                break

    def search_call(self) -> list:
        fwds = []
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']['dots'][self.API_KEY]

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if dot['type']['forward']['selected'] in [1, '1', True]:
                    dot.pop('type')
                    dot['uuid'] = uuid
                    fwds.append(dot)

        return fwds

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
        for field in ['domain', 'target', 'enabled', 'port']:
            if self.fwd[field] != self.p[field]:
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
    def _simplify_existing(fwd: dict) -> dict:
        # makes processing easier
        return {
            'uuid': fwd['uuid'],
            'domain': fwd['domain'],
            'target': fwd['server'],
            'port': fwd['port'],
            'enabled': fwd['enabled'] in [1, '1', True],
        }

    def _build_diff_after(self) -> dict:
        return {
            'uuid': self.fwd['uuid'] if 'uuid' in self.fwd else None,
            'domain': self.p['domain'],
            'target': self.p['target'],
            'port': self.p['port'],
            'enabled': self.p['enabled'],
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'type': 'forward',
                'enabled': 1 if self.p['enabled'] else 0,
                'domain': self.p['domain'],
                'server': self.p['target'],
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
