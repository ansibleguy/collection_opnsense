from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class SenderCanonical(BaseModule):
    FIELD_ID = 'address'
    CMDS = {
        'add': 'addSendercanonical',
        'del': 'delSendercanonical',
        'set': 'setSendercanonical',
        'search': 'get',
        'toggle': 'toggleSendercanonical',
    }
    API_KEY_PATH = 'sendercanonical.sendercanonicals.sendercanonical'
    API_MOD = 'postfix'
    API_CONT = 'sendercanonical'
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
    EXIST_ATTR = 'sender'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.sender = {}
