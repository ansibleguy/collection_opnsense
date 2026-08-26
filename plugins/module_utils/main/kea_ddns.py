from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip


class Ddns(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'ddns.general'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'kea'
    API_CONT = 'ddns'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'enabled', 'server_ip', 'server_port'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['server_port'],
    }
    INT_VALIDATIONS = {
        'server_port': {'min': 1, 'max': 65535},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def check(self) -> None:
        if not is_ip(self.p['server_ip']):
            self.m.fail_json('The provided IP is invalid!')

        self._base_check()
