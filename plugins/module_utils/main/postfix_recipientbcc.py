from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class RecipientBCC(BaseModule):
    FIELD_ID = 'address'
    CMDS = {
        'add': 'addRecipientbcc',
        'del': 'delRecipientbcc',
        'set': 'setRecipientbcc',
        'search': 'get',
        'toggle': 'toggleRecipientbcc',
    }
    API_KEY_PATH = 'recipientbcc.recipientbccs.recipientbcc'
    API_MOD = 'postfix'
    API_CONT = 'recipientbcc'
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
    EXIST_ATTR = 'recipient'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.recipient = {}
