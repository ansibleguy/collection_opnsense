from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Headercheck(BaseModule):
    FIELD_ID = 'expression'
    CMDS = {
        'add': 'addHeadercheck',
        'del': 'delHeadercheck',
        'set': 'setHeadercheck',
        'search': 'get',
        'toggle': 'toggleHeadercheck',
    }
    API_KEY_PATH = 'headerchecks.headerchecks.headercheck'
    API_MOD = 'postfix'
    API_CONT = 'headerchecks'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = []
    FIELDS_ALL = ['enabled', 'expression', 'filter']
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['filter'],
    }
    EXIST_ATTR = 'headercheck'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.headercheck = {}

    def check(self) -> None:
        self.find(match_fields=['expression', 'filter'])
