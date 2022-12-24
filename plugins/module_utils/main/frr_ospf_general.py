from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'ospf'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'carp', 'id', 'cost', 'enabled', 'passive_ints', 'redistribute',
        'redistribute_map', 'originate', 'originate_always', 'originate_metric',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'carp': 'carp_demote',
        'id': 'routerid',
        'cost': 'costreference',
        'originate_always': 'originatealways',
        'originate_metric': 'originatemetric',
        'passive_ints': 'passiveinterfaces',
        'redistribute_map': 'redistributemap',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'carp', 'originate', 'originate_always'],
        'list': ['passive_ints', 'redistribute'],
        'select': ['redistribute_map'],
        'int': ['originate_metric', 'cost'],
    }
    FIELDS_IGNORE = ['prefixlists', 'routemaps', 'networks', 'interfaces']
    INT_VALIDATIONS = {
        'cost': {'min': 1, 'max': 4294967},
        'originate_metric': {'min': 0, 'max': 16777214},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)