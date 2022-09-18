from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_matching, is_true, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Test:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addTest',
        'del': 'delTest',
        'set': 'setTest',
        'search': 'get',
    }
    API_MAIN_KEY = 'monit'
    API_KEY = 'test'
    API_MOD = 'monit'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['type', 'condition', 'action', 'path']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'test'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.test = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_tests = None
        self.b = Base(instance=self)

    def check(self):
        if self.p['state'] == 'present':
            if self.p['condition'] is None:
                self.m.fail_json(
                    "You need to provide a 'condition' to create a test!"
                )

            if self.p['action'] == 'execute' and self.p['path'] == '':
                self.m.fail_json(
                    "You need to provide the path to a executable to "
                    "create a test of type 'execute'!"
                )

        # checking if item exists
        self._find_test()
        if self.exists:
            self.call_cnf['params'] = [self.test['uuid']]

        self.r['diff']['after'] = self._build_diff(data=self.p)

    def _find_test(self):
        if self.existing_tests is None:
            self.existing_tests = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_tests,
            compare_item=self.p, match_fields=[self.FIELD_ID],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.test = match
            self.r['diff']['before'] = self._build_diff(data=self.test)
            self.exists = True

    @staticmethod
    def _simplify_existing(test: dict) -> dict:
        # makes processing easier
        return {
            'uuid': test['uuid'],
            'name': test['name'],
            'type': get_selected(test['type']),
            'condition': test['condition'],
            'action': get_selected(test['action']),
            'path': test['path'],
        }

    def _build_diff(self, data: dict) -> dict:
        return self.b.build_diff(data=data)

    def process(self):
        self.b.process()

    def _search_call(self) -> list:
        return self.b.search()

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
