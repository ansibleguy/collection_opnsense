from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Bridge(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY_PATH = 'bridge.bridged'
    API_KEY_PATH_REQ = 'bridge'
    API_MOD = 'interfaces'
    API_CONT = 'bridge_settings'
    FIELDS_CHANGE = [
        'members', 'link_local', 'stp', 'stp_proto', 'stp_interfaces', 'stp_max_age', 'stp_fwdelay', 'stp_hold',
        'cache_size', 'cache_timeout', 'span_interfaces', 'edge_interfaces', 'auto_edge_interfaces',
        'ptp_interfaces', 'auto_ptp_interfaces', 'static_interfaces', 'private_interfaces',
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'description': 'descr',
        'link_local': 'linklocal',
        'stp': 'enablestp',
        'stp_proto': 'proto',
        'stp_interfaces': 'stp',
        'stp_max_age': 'maxage',
        'stp_fwdelay': 'fwdelay',
        'stp_hold': 'holdcnt',
        'cache_size': 'maxaddr',
        'cache_timeout': 'timeout',
        'span_interfaces': 'span',
        'edge_interfaces': 'edge',
        'auto_edge_interfaces': 'autoedge',
        'ptp_interfaces': 'ptp',
        'auto_ptp_interfaces': 'autoptp',
        'static_interfaces': 'static',
        'private_interfaces': 'private',
    }
    FIELDS_TYPING = {
        'bool': ['link_local', 'stp'],
        'list': [
            'members', 'stp_interfaces', 'span_interfaces', 'edge_interfaces', 'auto_edge_interfaces',
            'ptp_interfaces', 'auto_ptp_interfaces', 'static_interfaces', 'private_interfaces',
        ],
        'select': ['stp_proto'],
        'int': ['stp_max_age', 'stp_fwdelay', 'stp_hold', 'cache_size', 'cache_timeout'],
    }
    INT_VALIDATIONS = {
        'stp_max_age': {'min': 6, 'max': 40},
        'stp_fwdelay': {'min': 4, 'max': 30},
        'stp_hold': {'min': 1, 'max': 10},
    }
    EXIST_ATTR = 'bridge'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.bridge = {}
