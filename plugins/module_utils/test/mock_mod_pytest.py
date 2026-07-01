from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
    OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG


MOCK_MOD_ARGS = dict(
    description=dict(type='str', required=True),
    minutes=dict(type='str', required=False, default='0', aliases=['min', 'm']),
    hours=dict(type='str', required=False, default='0', aliases=['hour', 'h']),
    days=dict(type='str', required=False, default='*', aliases=['day', 'd']),
    months=dict(type='str', required=False, default='*', aliases=['month', 'M']),
    weekdays=dict(type='str', required=False, default='*', aliases=['wd']),
    who=dict(type='str', required=False, default='root'),
    command=dict(type='str', required=False, aliases=['cmd']),
    parameters=dict(type='str', required=False, aliases=['params']),
    **RELOAD_MOD_ARG,
    **STATE_MOD_ARG,
    **OPN_MOD_ARGS,
)


class MockOPNsenseModule(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_test',
        'del': 'del_test',
        'set': 'set_test',
        'search': 'get',
        'toggle': 'toggle_test',
    }
    API_KEY_PATH = 'test.tests.test'
    API_MOD = 'test'
    API_CONT = 'tests'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'minutes', 'hours', 'days', 'months',
        'weekdays', 'command', 'who', 'parameters'
    ]
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['command'],
        'int': ['minutes', 'hours', 'days', 'months', 'weekdays'],
    }
    FIELDS_ALL = ['description', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'existing'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None, multi: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail, multi=multi)
        self.existing = {}
        self.available_commands = []

    def check(self) -> None:
        self._base_check()
