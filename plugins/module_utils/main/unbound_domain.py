from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_port, is_ip
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Domain(BaseModule):
    CMDS = {
        'add': 'addDomainOverride',
        'del': 'delDomainOverride',
        'set': 'setDomainOverride',
        'search': 'get',
        'toggle': 'toggleDomainOverride',
    }
    API_KEY_PATH = 'unbound.domains.domain'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'server', 'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
    }
    EXIST_ATTR = 'domain'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.domain = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_domain(module=self.m, domain=self.p['domain'])
            self._validate_server()

        self._base_check()

    def _validate_server(self) -> None:
        server = self.p['server']

        if server.find('@') != -1:
            server, port = self.p['server'].split('@', 1)
            validate_port(module=self.m, port=port)

        if not is_ip(server):
            self.m.fail_json(f"Value '{server}' is not a valid IP-address!")
