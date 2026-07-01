from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class OneToOne(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_rule',
        'del': 'del_rule',
        'set': 'set_rule',
        'search': 'get',
        'toggle': 'toggle_rule',
    }
    API_KEY_PATH = 'filter.onetoone.rule'
    API_MOD = 'firewall'
    API_CONT = 'one_to_one'
    FIELDS_CHANGE = [
        'log', 'sequence', 'interface', 'type', 'source_net', 'source_invert', 'destination_net', 'destination_invert',
        'external', 'nat_reflection', 'description'

    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'source_invert': 'source_not',
        'destination_invert': 'destination_not',
        'nat_reflection': 'natreflection',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'log', 'source_invert', 'destination_invert'],
        'list': [],
        'select': ['interface', 'type', 'nat_reflection'],
        'int': [],
    }
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 99999},
    }
    EXIST_ATTR = 'rule'
    API_CMD_REL = 'apply'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.rule = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['interface']):
                self.m.fail_json(
                    "You need to provide an 'interface' to create a one-to-one"
                )

        self.find(match_fields=self.p['match_fields'])

        self._base_check()
