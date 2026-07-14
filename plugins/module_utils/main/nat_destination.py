from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class DNat(BaseModule):
    CMDS = {
        'add': 'add_rule',
        'del': 'del_rule',
        'set': 'set_rule',
        'search': 'get',
        'toggle': 'toggle_rule',
    }
    API_KEY_PATH = 'DNat.rule'
    API_MOD = 'firewall'
    API_CONT = 'd_nat'
    FIELDS_CHANGE = [
        'sequence', 'no_port_forward', 'interface', 'ip_protocol', 'protocol',
        'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port',
        'target', 'local_port', 'pool_opts', 'log', 'description', 'tag', 'tagged',
        'nat_reflection', 'associated_rule',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_BOOL_INVERT = ['enabled']
    FIELDS_TRANSLATE = {
        'enabled': 'disabled',
        'no_port_forward': 'nordr',
        'ip_protocol': 'ipprotocol',
        'source_invert': ('source', 'not'),
        'source_net': ('source', 'network'),
        'source_port': ('source', 'port'),
        'destination_invert': ('destination', 'not'),
        'destination_net': ('destination', 'network'),
        'destination_port': ('destination', 'port'),
        'local_port': 'local-port',
        'pool_opts': 'poolopts',
        'description': 'descr',
        'nat_reflection': 'natreflection',
        'associated_rule': 'pass',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'log', 'no_port_forward', 'source_invert', 'destination_invert'],
        'list': ['interface'],
        'select': ['ip_protocol', 'protocol', 'pool_opts', 'nat_reflection', 'associated_rule'],
        'int': ['sequence'],
    }
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 999999},
    }
    EXIST_ATTR = 'rule'
    API_CMD_REL = 'apply'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.rule = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['target']):
                self.m.fail_json(
                    "You need to provide a 'target' to create a destination-nat rule!"
                )

        if not is_unset(self.p['protocol']):
            # OPNsense stores/returns 'protocol' lowercase (model enforces 'ChangeCase: lower') -
            # normalize here so diff-comparisons against the existing entry don't falsely report a change
            self.p['protocol'] = self.p['protocol'].lower()

        self.find(match_fields=self.p['match_fields'])

        self._base_check()
