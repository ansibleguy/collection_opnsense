from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_simple_existing, validate_int_fields, is_ip, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Service(BaseModule):
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
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['tests', 'depends'],
        'select': ['type', 'interface'],
        'int': ['service_timeout'],
    }
    EXIST_ATTR = 'service'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.service = {}
        self.existing_tests = None

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        if self.p['state'] == 'present':
            if is_unset(self.p['type']):
                self.m.fail_json("You need to provide a 'type' to create a service!")

            elif self.p['type'] == 'network' and is_unset(self.p['interface']) and is_unset(self.p['address']):
                self.m.fail_json(
                    "You need to provide either an 'interface' or 'address' "
                    "to create a network service!"
                )

            elif self.p['type'] == 'host' and is_unset(self.p['address']):
                self.m.fail_json(
                    "You need to provide an 'address' to create "
                    "a remote-host service!"
                )

            if self.p['address'] != '' and not is_ip(self.p['address']):
                self.m.fail_json(
                    f"The address value '{self.p['address']}' is not a valid IP!"
                )

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.service['uuid']]

        if self.p['state'] == 'present':
            self.p['tests'] = self._find_tests()
            self.p['depends'] = self._find_dependencies()
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

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
            if len(self.existing_entries) > 0:
                for uuid, svc in self.existing_entries.items():
                    existing[svc['name']] = uuid

            for svc in self.p['depends']:
                if svc not in existing:
                    self.m.fail_json(f"Dependency '{svc}' does not exist!")

                services.append(existing[svc])

        return services

    def get_existing(self) -> list:
        # pylint: disable=W0212
        existing = get_simple_existing(
            entries=self._search_call(),
            simplify_func=self.b._simplify_existing
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
