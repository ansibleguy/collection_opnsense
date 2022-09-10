from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    get_matching, is_true, to_digit, get_simple_existing
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_helper import \
    validate_domain, reconfigure


class Alias:
    CMDS = {
        'add': 'addHostAlias',
        'del': 'delHostAlias',
        'set': 'setHostAlias',
        'search': 'get',
    }
    API_KEY = 'alias'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.alias = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
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
        validate_domain(module=self.m, domain=self.p['domain'])

        # checking if item exists
        self._find_alias()
        self._find_target()
        if self.p['state'] == 'present' and self.target is None:
            self.m.fail_json(f"Alias-target '{self.p['target']}' was not found!")

        self.r['diff']['after'] = self._build_diff_after()

    def _find_alias(self):
        if self.existing_aliases is None:
            self.existing_aliases = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_aliases,
            compare_item=self.p, match_fields=self.p['match_fields'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.alias = match
            self.exists = True
            self.r['diff']['before'] = self.alias
            self.call_cnf['params'] = [self.alias['uuid']]

    def _find_target(self):
        if len(self.existing_hosts) > 0:
            for uuid, host in self.existing_hosts.items():
                if f"{host['hostname']}.{host['domain']}" == self.p['target']:
                    self.target = uuid
                    break

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

    def _search_call(self) -> dict:
        unbound = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']
        self.existing_hosts = unbound['hosts']['host']
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
        check_fields = ['target', 'domain', 'alias',  'description', 'enabled']

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
        simple = {
            'enabled': is_true(alias['enabled']),
            'domain': alias['domain'],
            'uuid': alias['uuid'],
            'alias': alias['hostname'],
            'description': alias['description'],
        }

        if len(alias['host']) > 0:
            simple['target'] = [v['value'] for v in alias['host'].values()][0]

        return simple

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
                'enabled': to_digit(self.p['enabled']),
                'hostname': self.p['alias'],
                'host': self.target,
                'domain': self.p['domain'],
                'description': self.p['description'],
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
        reconfigure(self)
