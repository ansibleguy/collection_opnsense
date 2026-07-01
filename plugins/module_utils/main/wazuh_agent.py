from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class WazuhAgent(GeneralModule):
    CMDS = {
        'search': 'get',
        'set': 'set',
    }
    API_KEY_PATH = 'agent'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'wazuhagent'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        # General section
        'enabled': ('general', 'enabled'),
        'server_address': ('general', 'server_address'),
        'agent_name': ('general', 'agent_name'),
        'protocol': ('general', 'protocol'),
        'port': ('general', 'port'),
        'debug_level': ('general', 'debug_level'),
        # Auth section
        'auth_password': ('auth', 'password'),
        'auth_port': ('auth', 'port'),
        # Logcollector section
        'remote_commands': ('logcollector', 'remote_commands'),
        'suricata_eve_log': ('logcollector', 'suricata_eve_log'),
        'syslog_programs': ('logcollector', 'syslog_programs'),
        # Module sections
        'rootcheck_enabled': ('rootcheck', 'enabled'),
        'syscollector_enabled': ('syscollector', 'enabled'),
        'syscheck_enabled': ('syscheck', 'enabled'),
        'active_response_enabled': ('active_response', 'enabled'),
        'active_response_remote_commands': ('active_response', 'remote_commands'),
        'active_response_fw_alias_ignore': ('active_response', 'fw_alias_ignore'),
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_DIFF_NO_LOG = ['auth_password']

    FIELDS_TYPING = {
        'bool': [
            'enabled', 'remote_commands', 'suricata_eve_log',
            'rootcheck_enabled', 'syscollector_enabled', 'syscheck_enabled',
            'active_response_enabled', 'active_response_remote_commands'
        ],
        'int': ['port', 'auth_port'],
        'list': ['syslog_programs', 'active_response_fw_alias_ignore'],
        'select': ['protocol'],
        'select_opt_list_idx': ['debug_level'],
    }
    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
        'auth_port': {'min': 1, 'max': 65535},
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
