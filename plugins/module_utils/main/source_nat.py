from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.rule import \
    validate_values
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class SNat(BaseModule):
    CMDS = {
        'add': 'addRule',
        'del': 'delRule',
        'set': 'setRule',
        'search': 'get',
        'toggle': 'toggleRule',
    }
    API_KEY = 'rule'
    API_KEY_1 = 'filter'
    API_KEY_2 = 'snatrules'
    API_MOD = 'firewall'
    API_CONT = 'source_nat'
    FIELDS_CHANGE = [
        'sequence', 'no_nat', 'interface', 'target', 'target_port', 'description',
        'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port', 'log',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'ip_protocol': 'ipprotocol',
        'source_invert': 'source_not',
        'destination_invert': 'destination_not',
        'no_nat': 'nonat',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'log', 'source_invert', 'no_nat', 'destination_invert'],
        'list': [],
        'select': ['interface', 'ip_protocol', 'protocol'],
        'int': [],
    }
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 99999},
    }
    EXIST_ATTR = 'rule'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.rule = {}
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        if self.p['state'] == 'present':
            if self.p['interface'] is None:
                self.m.fail_json(
                    "You need to provide an 'interface' to create a source-nat rule!"
                )

            if self.p['target'] is None:
                self.m.fail_json(
                    "You need to provide an 'target' to create a source-nat rule!"
                )

        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
        self._build_log_name()

        self.b.find(match_fields=self.p['match_fields'])
        if self.exists:
            self.call_cnf['params'] = [self.rule['uuid']]

        if self.p['state'] == 'present':
            validate_values(module=self.m, cnf=self.p, error_func=self.m.fail_json)
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _build_log_name(self) -> str:
        if self.p['description'] not in [None, '']:
            log_name = self.p['description']

        else:
            log_name = 'FROM '

            if self.p['source_invert']:
                log_name += 'NOT '

            log_name += f"{self.p['source_net']} <= PROTO {self.p['protocol']} => "

            if self.p['destination_invert']:
                log_name += 'NOT '

            log_name += f"{self.p['destination_net']}:{self.p['destination_port']} "
            log_name += f" =NAT=> {self.p['target']}:{self.p['target_port']}"

        return log_name
