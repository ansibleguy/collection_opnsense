from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    is_ip, get_matching, is_true, to_digit, get_simple_existing
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_helper import \
    validate_domain, reload


class Domain:
    CMDS = {
        'add': 'addDomainOverride',
        'del': 'delDomainOverride',
        'set': 'setDomainOverride',
        'search': 'get',
    }
    API_KEY = 'domain'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    CHANGE_CHECK_FIELDS = ['domain', 'server', 'description', 'enabled']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.domain = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_domains = None

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
        if not is_ip(self.p['server']):
            self.m.fail_json(f"Server-value '{self.p['server']}' not a valid IP-address!")

        # checking if item exists
        self._find_domain()
        if self.exists:
            self.call_cnf['params'] = [self.domain['uuid']]

        self.r['diff']['after'] = self._build_diff_after()

    def _find_domain(self):
        if self.existing_domains is None:
            self.existing_domains = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_domains,
            compare_item=self.p, match_fields=self.p['match_fields'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.domain = match
            self.r['diff']['before'] = self.domain
            self.exists = True

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

    def _search_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']['domains'][self.API_KEY]

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
        for field in set(self.CHANGE_CHECK_FIELDS) - set(self.p['match_fields']):
            if str(self.domain[field]) != str(self.p[field]):
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
    def _simplify_existing(domain: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(domain['enabled']),
            'uuid': domain['uuid'],
            'domain': domain['domain'],
            'server': domain['server'],
            'description': domain['description'],
        }

    def _build_diff_after(self) -> dict:
        return {
            'uuid': self.domain['uuid'] if 'uuid' in self.domain else None,
            'enabled': self.p['enabled'],
            'domain': self.p['domain'],
            'server': self.p['server'],
            'description': self.p['description'],
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'enabled': to_digit(self.p['enabled']),
                'domain': self.p['domain'],
                'server': self.p['server'],
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

    def reload(self):
        # reload running config
        reload(self)
