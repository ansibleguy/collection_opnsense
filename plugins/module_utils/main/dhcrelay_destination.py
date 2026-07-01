from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class DhcRelayDestination(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_dest',
        'del': 'del_dest',
        'set': 'set_dest',
        'search': 'get',
    }
    API_KEY_PATH = 'dhcrelay.destinations'
    API_KEY_PATH_REQ = 'destination'
    API_MOD = 'dhcrelay'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['server']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'list': ['server'],
    }
    EXIST_ATTR = 'destination'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.destination = {}

    def check(self) -> None:

        if self.p['state'] == 'present':
            if is_unset(self.p['server']):
                self.m.fail_json("You need to provide list of 'server' to create a dhcrelay_destination!")

        self._base_check()
