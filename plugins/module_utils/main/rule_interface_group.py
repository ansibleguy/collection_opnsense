from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Group(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
    }
    API_KEY_PATH = 'group.ifgroupentry'
    API_KEY_PATH_REQ = 'group'
    API_MOD = 'firewall'
    API_CONT = 'group'
    FIELDS_CHANGE = ['name', 'members', 'gui_group', 'sequence', 'description']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_BOOL_INVERT = ['gui_group']
    FIELDS_TRANSLATE = {
        'name': 'ifname',
        'description': 'descr',
        'gui_group': 'nogroup'
    }
    FIELDS_TYPING = {
        'bool': ['gui_group'],
        'list': ['members'],
        'select': ['members'],
        'int': ['sequence'],
    }
    INT_VALIDATIONS = {
        'sequence': {'min': 0, 'max': 9999},
    }
    EXIST_ATTR = 'group'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.group = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['members']):
                self.m.fail_json("You need to provide a 'members' to create a rule interface group!")

        self._base_check()

    def update(self) -> None:
        self._base_update(enable_switch=False)
