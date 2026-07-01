from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Loopback(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
    }
    API_KEY_PATH = 'loopback.loopback'
    API_MOD = 'interfaces'
    API_CONT = 'loopback_settings'
    FIELDS_CHANGE = []
    FIELDS_ALL = [FIELD_ID]
    FIELDS_TYPING = {}
    EXIST_ATTR = 'interface'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None,):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.interface = {}

    def check(self) -> None:
        self._base_check()
