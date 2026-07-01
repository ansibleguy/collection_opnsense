from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Tag(BaseModule):
    FIELD_ID = 'tag'
    CMDS = {
        'add': 'add_tag',
        'del': 'del_tag',
        'search': 'get',
    }
    API_KEY_PATH = 'dnsmasq.dhcp_tags'
    API_KEY_PATH_REQ = 'tag'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = []
    FIELDS_TYPING = {}
    FIELDS_ALL = ['tag']
    EXIST_ATTR = 'tag'
    STR_VALIDATIONS = {
        'tag': r'^[0-9a-zA-Z]{1,1024}$'
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.tag = {}
