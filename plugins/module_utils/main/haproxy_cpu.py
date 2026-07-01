from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyCpu(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addCpu',
        'del': 'delCpu',
        'set': 'setCpu',
        'search': 'get',
        'toggle': 'toggleCpu',
    }
    API_KEY_PATH = 'haproxy.cpus.cpu'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = ['enabled', 'name', 'thread_id', 'cpu_id']
    FIELDS_ALL = FIELDS_CHANGE

    EXIST_ATTR = 'cpu'

    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['thread_id'],
        'list': ['cpu_id'],
    }

    STR_VALIDATIONS = {
        'name': r'^[0-9a-zA-Z._-]{1,255}$',  # Name validation from XML model
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.cpu = {}
