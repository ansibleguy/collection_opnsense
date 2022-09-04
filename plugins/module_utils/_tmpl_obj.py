from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session


class TMPL:
    FIELD_ID = 'stuff_name'
    CMDS = {
        'add': 'addstuff',
        'del': 'delStuff',
        'set': 'setstuff',
        'search': 'searchstuff',
        'detail': 'getstuff',
        'toggle': 'togglestuff',
    }
    API_KEY = 'stuff'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.stuff = {}
        self.call_cnf = {  # config shared by all calls
            'module': 'API-Module',
            'controller': 'API-Controller',
        }
        self.existing_stuff = None

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
        # checking if item exists
        self._find_stuff()
        if self.exists:
            self.call_cnf['params'] = [self.stuff['uuid']]

        self.r['diff']['after'] = self._build_diff_after()

        # basic validation of conditional parameters
        if not self.exists and self.p['state'] == 'present':
            if self.p['value'] is None or len(self.p['value']) == 0:
                self.m.fail_json('You need to provide values to create stuff!')

    def _find_stuff(self):
        if self.existing_stuff is None:
            self.existing_stuff = self.search_call()

        for existing in self.existing_stuff:
            _matching = []
            existing = self._simplify_existing(existing)

            for field in []:  # match_fields
                _matching.append(existing[field] == self.p[field])

            if all(_matching):
                self.stuff = existing
                self.r['diff']['before'] = self.stuff
                self.exists = True
                break

    def _error(self, msg: str):
        # for special handling of errors
        self.m.fail_json(msg)

    def search_call(self) -> list:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['rows']

    def detail_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['detail']}
        })['stuff']

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
        for field in []:
            if str(self.stuff[field]) != str(self.p[field]):
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
    def _simplify_existing(stuff: dict) -> dict:
        # makes processing easier
        return {
            'param1': stuff['param1'],
            'param2': stuff['param2'],
        }

    def _build_diff_after(self) -> dict:
        return {
            'param1': self.p['param1'],
            'param2': self.p['param2'],
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'param1': self.p['param1'],
                'param2': self.p['param2'],
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

    def enable(self):
        if self.exists and self.stuff['enabled'] != '1':
            self.r['changed'] = True
            self.r['diff']['before'] = {self.p[self.FIELD_ID]: {'enabled': False}}
            self.r['diff']['after'] = {self.p[self.FIELD_ID]: {'enabled': True}}

            if not self.m.check_mode:
                self._change_enabled_state(1)

    def disable(self):
        if (self.exists and self.stuff['enabled'] != '0') or not self.exists:
            self.r['changed'] = True
            self.r['diff']['before'] = {self.p[self.FIELD_ID]: {'enabled': True}}
            self.r['diff']['after'] = {self.p[self.FIELD_ID]: {'enabled': False}}

            if not self.m.check_mode:
                self._change_enabled_state(0)

    def _change_enabled_state(self, value: int):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': self.CMDS['toggle'],
                'params': [self.stuff['uuid'], value],
            }
        })
