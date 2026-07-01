from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Service(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_service',
        'del': 'del_service',
        'set': 'set_service',
        'search': 'get',
        'toggle': 'toggle_service',
    }
    API_KEY_PATH = 'monit.service'
    API_MOD = 'monit'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.service = {}
        self.existing_tests = None

    def check(self) -> None:
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

            if not is_unset(self.p['address']) and not is_ip(self.p['address']):
                self.m.fail_json(
                    f"The address value '{self.p['address']}' is not a valid IP!"
                )

        self.find(match_fields=[self.FIELD_ID])

        if self.p['state'] == 'present':
            self.find_multiple_links(
                field='tests',
                existing=self.existing_tests,
            )
            self.find_multiple_links(
                field='depends',
                existing=self.existing_entries,
            )

        self._base_check()
