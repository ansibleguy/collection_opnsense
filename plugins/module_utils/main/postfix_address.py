from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Address(BaseModule):
    FIELD_ID = 'address'
    CMDS = {
        'add': 'addAddress',
        'del': 'delAddress',
        'set': 'setAddress',
        'search': 'get',
        'toggle': 'toggleAddress',
    }
    API_KEY_PATH = 'address.addresses.address'
    API_MOD = 'postfix'
    API_CONT = 'address'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['to']
    FIELDS_ALL = ['enabled', 'address']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {'address': 'from'}
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['to'],
    }
    EXIST_ATTR = 'address'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.address = {}
