from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyResolver(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addResolver',
        'del': 'delResolver',
        'set': 'setResolver',
        'search': 'get',
        'toggle': 'toggleResolver',
    }
    API_KEY_PATH = 'haproxy.resolvers.resolver'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = [
        'enabled', 'name', 'description', 'nameservers', 'parse_resolv_conf',
        'resolve_retries', 'timeout_resolve', 'timeout_retry', 'accepted_payload_size',
        'hold_valid', 'hold_obsolete', 'hold_refused', 'hold_nx', 'hold_timeout', 'hold_other'
    ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'parse_resolv_conf'],
        'list': ['nameservers'],
        'int': ['resolve_retries', 'accepted_payload_size'],
    }

    EXIST_ATTR = 'haproxy_resolver'

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
        'description': r'^.{1,255}$',
    }

    INT_VALIDATIONS = {
        'resolve_retries': {'min': 0, 'max': 100000},
        'accepted_payload_size': {'min': 0, 'max': 65535},
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_resolver = {}
