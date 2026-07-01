from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Lagg(BaseModule):
    FIELD_ID = 'device'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
    }
    API_KEY_PATH = 'lagg.lagg'
    API_MOD = 'interfaces'
    API_CONT = 'lagg_settings'
    FIELDS_CHANGE = [
        'members', 'primary_member', 'proto', 'lacp_fast_timeout', 'use_flowid',
        'lagghash', 'lacp_strict', 'mtu', 'description'
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'device': 'laggif',
        'description': 'descr',
    }
    FIELDS_TYPING = {
        'bool': ['lacp_fast_timeout'],
        'list': ['members', 'lagghash'],
        'select': ['members', 'primary_member', 'proto', 'use_flowid', 'lagghash', 'lacp_strict'],
    }
    INT_VALIDATIONS = {
        'mtu': {'min': 576, 'max': 65535},
    }
    EXIST_ATTR = 'lagg'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.lagg = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['members']):
                self.m.fail_json("You need to provide a list of 'members' to create a lagg!")

            if self.p['proto'] in ['lacp', 'loadbalance'] and is_unset(self.p['lagghash']):
                self.m.fail_json("You need to provide a list of 'lagghash' to create a lagg!")

        self._base_check()

    def update(self) -> None:
        self._base_update(enable_switch=False)
