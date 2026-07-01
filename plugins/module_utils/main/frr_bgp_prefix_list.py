from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Prefix(BaseModule):
    CMDS = {
        'add': 'addPrefixlist',
        'del': 'delPrefixlist',
        'set': 'setPrefixlist',
        'search': 'get',
        'toggle': 'togglePrefixlist',
    }
    API_KEY_PATH = 'bgp.prefixlists.prefixlist'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['network', 'description', 'version', 'action']
    FIELDS_MATCH = ['seq', 'name']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_MATCH)
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'seq': 'seqnumber',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['version', 'action'],
    }
    INT_VALIDATIONS = {
        'seq': {'min': 1, 'max': 4294967294},
    }
    STR_VALIDATIONS = {
        'name': r'^[a-zA-Z0-9._-]{1,64}$'
    }
    EXIST_ATTR = 'prefix_list'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.prefix_list = {}
        self.existing_prefixes = None
        self.existing_maps = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['network']) or is_unset(self.p['seq']) or is_unset(self.p['action']):
                self.m.fail_json(
                    'To create a BGP prefix-list you need to provide a network, '
                    'sequence-number and action!'
                )

        self._base_check(match_fields=self.FIELDS_MATCH)
