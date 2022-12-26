from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Alias(BaseModule):
    CMDS = {
        'add': 'addHostAlias',
        'del': 'delHostAlias',
        'set': 'setHostAlias',
        'search': 'get',
        'toggle': 'toggleHostAlias',
    }
    API_KEY = 'alias'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.alias = {}
        self.existing_hosts = None
        self.target_found = False

    def check(self):
        if self.p['state'] == 'present':
            if is_unset(self.p['target']):
                self.m.fail_json(
                    "You need to provide a 'target' if you want to create a host-alias!"
                )

            validate_domain(module=self.m, domain=self.p['domain'])

        self.b.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            self._find_target()

            if not self.target_found:
                self.m.fail_json(f"Alias-target '{self.p['target']}' was not found!")

            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _find_target(self):
        if len(self.existing_hosts) > 0:
            for uuid, host in self.existing_hosts.items():
                if f"{host['hostname']}.{host['domain']}" == self.p['target']:
                    self.target_found = True
                    self.p['target'] = uuid
                    break

    def _search_call(self) -> dict:
        unbound = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']
        self.existing_hosts = unbound['hosts']['host']
        return unbound['aliases'][self.API_KEY]
