from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Domain(BaseModule):
    FIELD_ID = 'domainname'
    CMDS = {
        'add': 'addDomain',
        'del': 'delDomain',
        'set': 'setDomain',
        'search': 'get',
        'toggle': 'toggleDomain',
    }
    API_KEY_PATH = 'domain.domains.domain'
    API_MOD = 'postfix'
    API_CONT = 'domain'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['destination']
    FIELDS_ALL = ['enabled', 'domainname']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
    }
    EXIST_ATTR = 'domain'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.domain = {}
