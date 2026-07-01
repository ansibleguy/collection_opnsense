from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class ControlAgent(GeneralModule):
    FIELD_ID = 'ip'
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'ctrlagent.general'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'kea'
    API_CONT = 'ctrl_agent'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'enabled', 'http_host', 'http_port'
    ]
    FIELDS_ALL = [*FIELDS_CHANGE]
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['http_port'],
    }
    INT_VALIDATIONS = {
        'http_port': {'min': 1, 'max': 65535},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def check(self) -> None:
        if not is_ip(self.p['http_host']):
            self.m.fail_json('The provided IP is invalid!')

        self._base_check()
