from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset


class UpstreamServer(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addupstreamserver',
        'del': 'delupstreamserver',
        'detail': 'getupstreamserver',
        'search': 'searchupstreamserver',
        'set': 'setupstreamserver',
    }
    API_KEY_PATH = 'upstream_server'
    API_MOD = 'nginx'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'description', 'server', 'port', 'priority',
        'max_conns', 'max_fails', 'fail_timeout', 'no_use'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'select': ['no_use'],
    }
    INT_VALIDATIONS = {
        'priority': {'min': 0, 'max': 1000000000},
        'port': {'min': 1, 'max': 65535},
    }
    EXIST_ATTR = 'upstream_server'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.upstream_server = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['port']) or is_unset(self.p['priority']) or is_unset(self.p['server']):
                self.m.fail_json(
                    "You need to provide a 'port', 'server' and 'priority' to create a server!"
                )

        self._base_check()

    def update(self) -> None:
        self._base_update(enable_switch=False)
