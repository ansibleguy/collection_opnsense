from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Recipient(BaseModule):
    FIELD_ID = 'address'
    CMDS = {
        'add': 'addRecipient',
        'del': 'delRecipient',
        'set': 'setRecipient',
        'search': 'get',
        'toggle': 'toggleRecipient',
    }
    API_KEY_PATH = 'recipient.recipients.recipient'
    API_MOD = 'postfix'
    API_CONT = 'recipient'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['action']
    FIELDS_ALL = ['enabled', 'address']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
    }
    EXIST_ATTR = 'recipient'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.recipient = {}
