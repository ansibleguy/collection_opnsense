from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_matching, is_true, get_simple_existing, validate_int_fields, \
    get_selected, get_selected_list, is_ip
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Service:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addService',
        'del': 'delService',
        'set': 'setService',
        'search': 'get',
        'toggle': 'toggleService',
    }
    API_KEY = 'service'
    API_MOD = 'monit'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'type', 'pidfile', 'match', 'path', 'service_timeout', 'address', 'interface',
        'start', 'stop', 'tests', 'depends', 'polltime', 'description',
    ]
    FIELDS_ALL = ['name', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    INT_VALIDATIONS = {
        'service_timeout': {'min': 1, 'max': 86400},
    }
    FIELDS_TRANSLATE = {
        'service_timeout': 'timeout',
    }
    EXIST_ATTR = 'service'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.service = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_services = None
        self.existing_tests = None
        self.b = Base(instance=self)

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        if self.p['state'] == 'present':
            if self.p['type'] is None:
                self.m.fail_json("You need to provide a 'type' to create a service!")

            elif self.p['type'] == 'network' and self.p['interface'] == '' and self.p['address'] == '':
                self.m.fail_json(
                    "You need to provide either an 'interface' or 'address' "
                    "to create a network service!"
                )

            elif self.p['type'] == 'host' and self.p['address'] == '':
                self.m.fail_json(
                    "You need to provide an 'address' to create "
                    "a remote-host service!"
                )

            if self.p['address'] != '' and not is_ip(self.p['address']):
                self.m.fail_json(
                    f"The address value '{self.p['address']}' is not a valid IP!"
                )

        # checking if item exists
        self._find_service()
        if self.exists:
            self.call_cnf['params'] = [self.service['uuid']]

        if self.p['state'] == 'present':
            self.p['tests'] = self._find_tests()
            self.p['depends'] = self._find_dependencies()
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _find_service(self):
        if self.existing_services is None:
            self.existing_services = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_services,
            compare_item=self.p, match_fields=[self.FIELD_ID],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.service = match
            self.r['diff']['before'] = self.b.build_diff(data=self.service)
            self.exists = True

    def _find_tests(self) -> list:
        tests = []
        existing = {}

        if len(self.p['tests']) > 0:
            if len(self.existing_tests) > 0:
                for uuid, test in self.existing_tests.items():
                    existing[test['name']] = uuid

            for test in self.p['tests']:
                if test not in existing:
                    self.m.fail_json(f"Test '{test}' does not exist!")

                tests.append(existing[test])

        return tests

    def _find_dependencies(self) -> list:
        services = []
        existing = {}

        if len(self.p['depends']) > 0:
            if len(self.existing_services) > 0:
                for uuid, svc in self.existing_services.items():
                    existing[svc['name']] = uuid

            for svc in self.p['depends']:
                if svc not in existing:
                    self.m.fail_json(f"Dependency '{svc}' does not exist!")

                services.append(existing[svc])

        return services

    def get_existing(self) -> list:
        existing = get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

        for svc in existing:
            _tests = []
            for test in svc['tests']:
                _tests.append(self.existing_tests[test]['name'])

            _dep = []
            for dep in svc['depends']:
                _dep.append(existing[dep]['name'])

            svc['tests'] = _tests
            svc['depends'] = _dep

        return existing

    def _search_call(self) -> list:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['monit']
        self.existing_tests = raw['test']
        return raw[self.API_KEY]

    @staticmethod
    def _simplify_existing(service: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(service['enabled']),
            'uuid': service['uuid'],
            'name': service['name'],
            'type': get_selected(service['type']),
            'pidfile': service['pidfile'],
            'match': service['match'],
            'path': service['path'],
            'service_timeout': int(service['timeout']),
            'address': service['address'],
            'interface': get_selected(service['interface']),
            'start': service['start'],
            'stop': service['stop'],
            'tests': get_selected_list(service['tests']),
            'depends': get_selected_list(service['depends']),
            'polltime': service['polltime'],
            'description': service['description'],
        }

    def process(self):
        self.b.process()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
