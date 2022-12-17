from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Community:
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addCommunitylist',
        'del': 'delCommunitylist',
        'set': 'setCommunitylist',
        'search': 'get',
        'toggle': 'toggleCommunitylist',
    }
    API_KEY = 'communitylist'
    API_KEY_1 = 'bgp'
    API_KEY_2 = 'communitylists'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['number', 'seq', 'action', 'community']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'seq': 'seqnumber',
    }
    INT_VALIDATIONS = {
        'number': {'min': 1, 'max': 500},
        'seq': {'min': 10, 'max': 99},
    }
    EXIST_ATTR = 'community_list'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.community_list = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.b = Base(instance=self)
        self.existing_entries = None

    def check(self):
        if self.p['state'] == 'present':
            if self.p['number'] in ['', None] or self.p['seq'] in ['', None] or self.p['action'] in ['', None]:
                self.m.fail_json(
                    'To create a BGP community-list you need to provide a number, '
                    'sequence-number and action!'
                )

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.community_list['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def process(self):
        self.b.process()

    @staticmethod
    def _simplify_existing(community_list: dict) -> dict:
        # makes processing easier
        return {
            'description': community_list['description'],
            'number': community_list['number'],
            'seq': community_list['seqnumber'],
            'community': community_list['community'],
            'action': get_selected(community_list['action']),
            'enabled': is_true(community_list['enabled']),
            'uuid': community_list['uuid'],
        }

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
