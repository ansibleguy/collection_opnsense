from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Prefix(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addPrefixlist',
        'del': 'delPrefixlist',
        'set': 'setPrefixlist',
        'search': 'get',
        'toggle': 'togglePrefixlist',
    }
    API_KEY_PATH = 'ospf.prefixlists.prefixlist'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['seq', 'action', 'network']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    INT_VALIDATIONS = {
        'seq': {'min': 10, 'max': 99},
    }
    FIELDS_TRANSLATE = {
        'seq': 'seqnumber',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
    }
    EXIST_ATTR = 'prefix'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.prefix = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['seq']) or is_unset(self.p['action']) or is_unset(self.p['network']):
                self.m.fail_json(
                    'To create a OSPF prefix-list you need to provide its sequence-number, '
                    'action and network!'
                )

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()
