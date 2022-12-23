from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, validate_str_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Prefix(BaseModule):
    CMDS = {
        'add': 'addPrefixlist',
        'del': 'delPrefixlist',
        'set': 'setPrefixlist',
        'search': 'get',
        'toggle': 'togglePrefixlist',
    }
    API_KEY = 'prefixlist'
    API_KEY_1 = 'bgp'
    API_KEY_2 = 'prefixlists'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
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
    STR_LEN_VALIDATIONS = {
        'name': {'min': 1, 'max': 64}
    }
    EXIST_ATTR = 'prefix_list'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.prefix_list = {}
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_prefixes = None
        self.existing_maps = None

    def check(self):
        if self.p['state'] == 'present':
            if self.p['network'] in ['', None] or self.p['seq'] in ['', None] or self.p['action'] in ['', None]:
                self.m.fail_json(
                    'To create a BGP prefix-list you need to provide a network, '
                    'sequence-number and action!'
                )

            validate_str_fields(
                module=self.m, data=self.p,
                field_regex=self.STR_VALIDATIONS,
                field_minmax_length=self.STR_LEN_VALIDATIONS
            )
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=self.FIELDS_MATCH)
        if self.exists:
            self.call_cnf['params'] = [self.prefix_list['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def process(self):
        self.b.process()

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
