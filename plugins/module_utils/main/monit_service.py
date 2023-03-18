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
    API_KEY_PATH = 'monit.service'
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
    SEARCH_ADDITIONAL = {
        'existing_tests': 'monit.test',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.service = {}
        self.existing_tests = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

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

        if self.p['state'] == 'present':
            self.b.find_multiple_links(
                field='tests',
                existing=self.existing_tests,
            )
            self.b.find_multiple_links(
                field='depends',
                existing=self.existing_entries,
            )
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

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
