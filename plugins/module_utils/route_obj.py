from ipaddress import ip_network

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session


class Route:
    FIELD_ID = 'uuid'
    CMDS = {
        'add': 'addroute',
        'del': 'delroute',
        'set': 'setroute',
        'search': 'searchroute',
    }
    API_KEY = 'route'
    API_MOD = 'routes'
    API_CONT = 'routes'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.route = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_routes = None

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
        try:
            ip_network(self.p['network'])

        except ValueError:
            self.m.fail_json(f"Value '{self.p['network']}' is not a valid network!")

        # checking if item exists
        self._find_route()
        if self.exists:
            self.call_cnf['params'] = [self.route['uuid']]

        self.r['diff']['after'] = self._build_diff_after()

    def _find_route(self):
        if self.existing_routes is None:
            self.existing_routes = self.search_call()

        # check if configured is in existing
        for route in self.existing_routes:
            route = self._simplify_existing(route)
            _matching = []
            for field in self.p['match_fields']:
                _matching.append(route[field] == self.p[field])

                if self.p['debug'] and field == 'gateway' and route[field] != self.p[field]:
                    self.m.warn(f"GW NOT MATCHED: {route[field]} != {self.p[field]}")

            if all(_matching):
                self.route = route
                self.r['diff']['before'] = self.route
                self.exists = True
                break

    def search_call(self) -> list:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['rows']

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
        for field in ['network', 'gateway', 'description', 'enabled']:
            if self.route[field] != self.p[field]:
                self.r['changed'] = True
                break

        # update if changed
        if self.r['changed'] and not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['set'],
                    'data': self._build_request(),
                }
            })

            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

    @staticmethod
    def _simplify_existing(route: dict) -> dict:
        # makes processing easier
        return {
            'uuid': route['uuid'],
            'network': route['network'],
            'gateway': route['gateway'].rsplit('-', 1)[0].strip(),
            'description': route['descr'],
            'enabled': not route['disabled'] in [1, '1', True],
        }

    def _build_diff_after(self) -> dict:
        return {
            'uuid': self.route['uuid'] if 'uuid' in self.route else None,
            'network': self.p['network'],
            'gateway': self.p['gateway'],
            'description': self.p['description'],
            'enabled': self.p['enabled'],
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'network': self.p['network'],
                'gateway': self.p['gateway'],
                'descr': self.p['description'],
                'disabled': 0 if self.p['enabled'] else 1,
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
        # reload the active routes
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{'command': 'reconfigure', 'params': []}
            })
