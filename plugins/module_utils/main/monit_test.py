from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset


class Test(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addTest',
        'del': 'delTest',
        'set': 'setTest',
        'search': 'get',
    }
    API_KEY_PATH = 'monit.test'
    API_MOD = 'monit'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['type', 'condition', 'action', 'path']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'test'
    FIELDS_TYPING = {
        'select': ['type', 'action'],
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.test = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['condition']):
                self.m.fail_json(
                    "You need to provide a 'condition' to create a test!"
                )

            if self.p['action'] == 'execute' and is_unset(self.p['path']):
                self.m.fail_json(
                    "You need to provide the path to a executable to "
                    "create a test of type 'execute'!"
                )

        self._base_check()

    def update(self) -> None:
        self.b.update(enable_switch=False)
