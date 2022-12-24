from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'ospf6'
    API_MOD = 'quagga'
    API_CONT = 'ospf6settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'carp', 'id', 'enabled', 'redistribute',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'carp': 'carp_demote',
        'id': 'routerid',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'carp'],
        'list': ['redistribute'],
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
