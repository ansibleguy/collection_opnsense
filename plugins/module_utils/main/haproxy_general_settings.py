from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class HaproxyGeneralSettings(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'haproxy.general'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'graceful_stop': 'gracefulStop',
        'hard_stop_after': 'hardStopAfter',
        'close_spread_time': 'closeSpreadTime',
        'seamless_reload': 'seamlessReload',
        'show_intro': 'showIntro',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + ['enabled']
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'graceful_stop', 'seamless_reload', 'show_intro'],
        'int': ['hard_stop_after', 'close_spread_time'],
    }

    FIELDS_BOOL_INVERT = ['graceful_stop']

    INT_VALIDATIONS = {
        'hard_stop_after': {'min': 0, 'max': 86400},  # 0 to 24 hours in seconds
        'close_spread_time': {'min': 0, 'max': 3600},  # 0 to 1 hour in seconds
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
