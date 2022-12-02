from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected, validate_str_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Prefix:
    FIELD_ID = 'name'
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
    FIELDS_CHANGE = [
        'network', 'description', 'version', 'seq', 'action', 'enabled',
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'seq': 'seqnumber',
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
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.prefix_list = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.b = Base(instance=self)
        self.existing_entries = None
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

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.prefix_list['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def process(self):
        self.b.process()

    @staticmethod
    def _simplify_existing(prefix_list: dict) -> dict:
        # makes processing easier
        return {
            'name': prefix_list['name'],
            'network': prefix_list['network'],
            'description': prefix_list['description'],
            'version': get_selected(prefix_list['version']),
            'seq': prefix_list['seqnumber'],
            'action': get_selected(prefix_list['action']),
            'enabled': is_true(prefix_list['enabled']),
            'uuid': prefix_list['uuid'],
        }

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def enable(self):
        self.b.enable()

    def disable(self):
        self.b.disable()

    def reload(self):
        self.b.reload()
