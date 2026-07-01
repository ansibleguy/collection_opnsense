from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyMailer(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addMailer',
        'del': 'delMailer',
        'set': 'setMailer',
        'search': 'get',
        'toggle': 'toggleMailer',
    }
    API_KEY_PATH = 'haproxy.mailers.mailer'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = [
        'enabled', 'name', 'description', 'mailservers', 'sender',
        'recipient', 'loglevel', 'timeout', 'hostname'
    ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['mailservers'],
        'int': ['timeout'],
        'select': ['loglevel'],
    }

    EXIST_ATTR = 'haproxy_mailer'

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
        'description': r'^.{1,255}$',
    }

    INT_VALIDATIONS = {
        'timeout': {'min': 1, 'max': 10000},
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_mailer = {}
