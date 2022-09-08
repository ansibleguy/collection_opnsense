from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    is_ip, valid_hostname, get_matching, get_selected, is_true, to_digit
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_helper import \
    validate_domain, reconfigure


class Host:
    CMDS = {
        'add': 'addHostOverride',
        'del': 'delHostOverride',
        'set': 'setHostOverride',
        'search': 'get',
    }
    API_KEY = 'host'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.host = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_hosts = None

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
        if self.p['record_type'] == 'MX':
            if not valid_hostname(self.p['value']):
                self.m.fail_json(f"Value '{self.p['value']}' is not a valid hostname!")

        else:
            self.p['prio'] = None

            if not is_ip(self.p['value']):
                self.m.fail_json(f"Value '{self.p['value']}' is not a valid IP-address!")

        validate_domain(module=self.m, domain=self.p['domain'])

        # checking if item exists
        self._find_host()
        if self.exists:
            self.call_cnf['params'] = [self.host['uuid']]

        self.r['diff']['after'] = self._build_diff_after()

    def _find_host(self):
        if self.existing_hosts is None:
            self.existing_hosts = self.search_call()

        self.host = get_matching(
            module=self.m, existing_items=self.existing_hosts,
            compare_item=self.p, match_fields=self.p['match_fields'],
            simplify_func=self._simplify_existing,
        )

        if self.host is not None:
            self.r['diff']['before'] = self.host
            self.exists = True

    def search_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']['hosts'][self.API_KEY]

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
        check_fields = [
            'hostname', 'domain', 'record_type', 'prio', 'value',
            'description', 'enabled'
        ]

        for field in set(check_fields) - set(self.p['match_fields']):
            if str(self.host[field]) != str(self.p[field]):
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

    def _simplify_existing(self, host: dict) -> dict:
        # makes processing easier
        data = {
            'enabled': is_true(host['enabled']),
            'hostname': host['hostname'],
            'uuid': host['uuid'],
            'domain': host['domain'],
            'description': host['description'],
            'record_type': get_selected(host['rr']),
        }

        if self.p['record_type'] == 'MX':
            data['prio'] = host['mxprio']
            data['value'] = host['mx']

        else:
            data['value'] = host['server']
            data['prio'] = None

        return data

    def _build_diff_after(self) -> dict:
        return {
            'uuid': self.host['uuid'] if 'uuid' in self.host else None,
            'enabled': self.p['enabled'],
            'hostname': self.p['hostname'],
            'domain': self.p['domain'],
            'record_type': self.p['record_type'],
            'value': self.p['value'],
            'prio': self.p['prio'],
            'description': self.p['description'],
        }

    def _build_request(self) -> dict:
        data = {
            'enabled': to_digit(self.p['enabled']),
            'hostname': self.p['hostname'],
            'domain': self.p['domain'],
            'rr': self.p['record_type'],  # A/AAAA/MX
            'description': self.p['description'],
        }

        if self.p['record_type'] == 'MX':
            data['mxprio'] = self.p['prio']
            data['mx'] = self.p['value']

        else:
            data['server'] = self.p['value']

        return {
            self.API_KEY: data
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
