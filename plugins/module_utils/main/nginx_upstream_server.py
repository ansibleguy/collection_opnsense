from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


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
    API_CMD_REL = 'reconfigure'
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
    FIELDS_IGNORE = []
    EXIST_ATTR = 'upstream_server'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.upstream_server = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['description']):
                self.m.fail_json('You need to supply a description!')

        self._base_check()

    def update(self) -> None:
        self.b.update(enable_switch=False)
