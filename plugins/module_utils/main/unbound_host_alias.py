from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Alias(BaseModule):
    CMDS = {
        'add': 'add_host_alias',
        'del': 'del_host_alias',
        'set': 'set_host_alias',
        'search': 'get',
        'toggle': 'toggle_host_alias',
    }
    API_KEY_PATH = 'unbound.aliases.alias'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['target', 'domain', 'alias',  'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'alias'
    FIELDS_TRANSLATE = {
        'target': 'host',
        'alias': 'hostname',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['target'],
    }
    SEARCH_ADDITIONAL = {
        'existing_hosts': 'unbound.hosts.host',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.alias = {}
        self.existing_hosts = None
        self.target_found = False

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['target']):
                self.m.fail_json(
                    "You need to provide a 'target' if you want to create a host-alias!"
                )

            validate_domain(module=self.m, domain=self.p['domain'])

        self.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            self._find_target()

            if not self.target_found:
                self.m.fail_json(f"Alias-target '{self.p['target']}' was not found!")

        self._base_check()

    def _find_target(self) -> None:
        if len(self.existing_hosts) > 0:
            for uuid, host in self.existing_hosts.items():
                if f"{host['hostname']}.{host['domain']}" == self.p['target']:
                    self.target_found = True
                    self.p['target'] = uuid
                    break
