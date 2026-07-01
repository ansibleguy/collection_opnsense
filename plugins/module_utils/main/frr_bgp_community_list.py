from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Community(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addCommunitylist',
        'del': 'delCommunitylist',
        'set': 'setCommunitylist',
        'search': 'get',
        'toggle': 'toggleCommunitylist',
    }
    API_KEY_PATH = 'bgp.communitylists.communitylist'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.community_list = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['number']) or is_unset(self.p['seq']) or is_unset(self.p['action']):
                self.m.fail_json(
                    'To create a BGP community-list you need to provide a number, '
                    'sequence-number and action!'
                )

        self._base_check()
