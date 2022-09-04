import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session


class Alias:
    CMDS = {
        'add': 'addHostAlias',
        'del': 'delDHostAlias',
        'set': 'setHostAlias',
        'search': 'get',
    }
    API_KEY = 'alias'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.alias = {}
        self.call_cnf = {  # config shared by all calls
            'module': 'unbound',
            'controller': 'settings',
        }
        self.existing_aliases = None
        self.existing_hosts = None
        self.target = None

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

        # checking if item exists
        self._find_alias()
        if self.exists:
            self.call_cnf['params'] = [self.alias['uuid']]

        self._find_target()
        if self.target is None:
            self.m.fail_json(f"Alias-target '{self.p['target']}' was not found!")

        self.r['diff']['after'] = self._build_diff_after()

    def _find_alias(self):
        if self.existing_aliases is None:
            self.existing_aliases = self.search_call()

        if len(self.existing_aliases) > 0:
            for uuid, existing in self.existing_aliases.items():
                _matching = []
                existing = self._simplify_existing(existing)

                for field in self.p['match_fields']:
                    _matching.append(existing[field] == self.p[field])

                if all(_matching):
                    existing['uuid'] = uuid
                    self.alias = existing
                    self.r['diff']['before'] = self.alias
                    self.exists = True
                    break

    def _find_target(self):
        for uuid, host in self.existing_hosts.items():
            if f"{host['hostname']}.{host['domain']}" == self.p['target']:
                self.target = uuid
                break

    def search_call(self) -> dict:
        unbound = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']
        self.existing_hosts = unbound['hosts']['host']
        # raise SystemExit(self.existing_hosts)
        return unbound['aliases'][self.API_KEY]

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
        check_fields = ['target', 'domain', 'alias',  'description']

        for field in set(check_fields) - set(self.p['match_fields']):
            if str(self.alias[field]) != str(self.p[field]):
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
    def _simplify_existing(alias: dict) -> dict:
        # makes processing easier
        return {
            'enabled': alias['enabled'] in [1, '1', True],
            'domain': alias['domain'],
            'alias': alias['hostname'],
            'description': alias['description'],
            'target': alias['host'],
        }

    def _build_diff_after(self) -> dict:
        return {
            'uuid': self.alias['uuid'] if 'uuid' in self.alias else None,
            'enabled': self.p['enabled'],
            'alias': self.p['alias'],
            'target': self.p['target'],
            'domain': self.p['domain'],
            'description': self.p['description'],
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'enabled': 1 if self.p['enabled'] else 0,
                'hostname': self.p['alias'],
                'host': self.target,
                'domain': self.p['domain'],
                'description': self.p['description'],
            }
        }

    def delete(self):
        # todo: bug deletion not working and getting jsonDecodeError (?!)
        bug = True

        if bug:
            self.p['enabled'] = False
            self.update()

        else:
            self.r['changed'] = True
            self.r['diff']['after'] = {}

            if not self.m.check_mode:
                self._delete_call()

                if self.p['debug']:
                    self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': self.CMDS['del']}})
