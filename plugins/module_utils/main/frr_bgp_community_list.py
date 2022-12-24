from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Community(BaseModule):
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
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
    }
    INT_VALIDATIONS = {
        'number': {'min': 1, 'max': 500},
        'seq': {'min': 10, 'max': 99},
    }
    EXIST_ATTR = 'community_list'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.community_list = {}

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
