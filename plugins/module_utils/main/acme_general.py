from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'acmeclient.settings'
    API_KEY_PATH_REQ = 'acmeclient.settings'
    API_MOD = 'acmeclient'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'auto_renewal', 'challenge_port', 'tls_challenge_port', 'restart_timeout',
        'haproxy_integration', 'log_level', 'show_intro',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'auto_renewal': 'autoRenewal',
        'challenge_port': 'challengePort',
        'tls_challenge_port': 'TLSchallengePort',
        'restart_timeout': 'restartTimeout',
        'haproxy_integration': 'haproxyIntegration',
        'log_level': 'logLevel',
        'show_intro': 'showIntro',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'auto_renewal', 'haproxy_integration', 'show_intro'],
        'select': ['log_level'],
        'int': ['challenge_port', 'tls_challenge_port', 'restart_timeout'],
    }
    INT_VALIDATIONS = {
        'challenge_port': {'min': 1024, 'max': 65535},
        'tls_challenge_port': {'min': 1024, 'max': 65535},
        'restart_timeout': {'min': 0, 'max': 86400},
    }
    EXIST_ATTR = 'settings'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
