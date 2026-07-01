from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Sender(BaseModule):
    FIELD_ID = 'address'
    CMDS = {
        'add': 'addSender',
        'del': 'delSender',
        'set': 'setSender',
        'search': 'get',
        'toggle': 'toggleSender',
    }
    API_KEY_PATH = 'sender.senders.sender'
    API_MOD = 'postfix'
    API_CONT = 'sender'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['action']
    FIELDS_ALL = ['enabled', 'address']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
    }
    EXIST_ATTR = 'sender'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.sender = {}
