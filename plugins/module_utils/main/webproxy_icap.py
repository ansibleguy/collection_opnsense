from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_1 = 'proxy'
    API_KEY_2 = 'forward'
    API_KEY = 'icap'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'request_url', 'response_url', 'ttl', 'send_client_ip', 'send_username',
        'encode_username', 'header_username', 'preview', 'preview_size', 'exclude',
        'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'enabled': 'enable',
        'request_url': 'RequestURL',
        'response_url': 'ResponseURL',
        'ttl': 'OptionsTTL',
        'send_client_ip': 'SendClientIP',
        'send_username': 'SendUsername',
        'encode_username': 'EncodeUsername',
        'header_username': 'UsernameHeader',
        'preview': 'EnablePreview',
        'preview_size': 'PreviewSize',
    }
    FIELDS_TYPING = {
        'list': ['exclude'],
        'bool': ['enabled', 'send_client_ip', 'send_username', 'encode_username', 'preview'],
        'int': ['ttl', 'preview_size']
    }
    STR_VALIDATIONS = {
        'header_username': r'^([a-zA-Z-]+)$'
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
