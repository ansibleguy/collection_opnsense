from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_port, is_true, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Forward(BaseModule):
    CMDS = {
        'add': 'addDot',
        'del': 'delDot',
        'set': 'setDot',
        'search': 'get',
        'toggle': 'toggleDot',
    }
    API_KEY = 'dot'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'target', 'port']
    FIELDS_ALL = ['type', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'server',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['port'],
    }
    EXIST_ATTR = 'fwd'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.fwd = {}
        self.call_headers = {
            'Referer': f"https://{self.p['firewall']}:{self.p['api_port']}/ui/unbound/forward",
        }
        # else the type will always be 'dns-over-tls':
        #   https://github.com/opnsense/core/commit/6832fd75a0b41e376e80f287f8ad3cfe599ea3d1

    def check(self) -> None:
        if not is_unset(self.p['domain']):
          validate_domain(module=self.m, domain=self.p['domain'])

        validate_port(module=self.m, port=self.p['port'])

        self.b.find(match_fields=['domain', 'target'])

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> list:
        fwds = []
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']['dots'][self.API_KEY]

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if is_true(dot['type']['forward']['selected']):
                    dot.pop('type')
                    dot['uuid'] = uuid
                    fwds.append(dot)

        return fwds
