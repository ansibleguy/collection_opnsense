from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get'
    }
    API_KEY_PATH = 'ipsec'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'ipsec'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'prefer_old_sa', 'disable_vpn_rules', 'passthrough_networks', 'authentication', 'local_group',
        'radius_servers', 'radius_accounting', 'radius_class_group', 'pam_service', 'pam_session',
        'pam_trim_email', 'charon_max_ikev1_exchanges', 'charon_threads', 'charon_ikesa_table_size',
        'charon_ikesa_table_segments', 'charon_init_limit_half_open', 'charon_ignore_acquire_ts',
        'charon_make_before_break', 'charon_install_routes', 'charon_cisco_unity', 'retransmit_tries',
        'retransmit_timeout', 'retransmit_base', 'retransmit_jitter', 'retransmit_limit',
        'syslog_log_name', 'syslog_log_level', 'syslog_app', 'syslog_asn',
        'syslog_cfg', 'syslog_chd', 'syslog_dmn', 'syslog_enc', 'syslog_esp', 'syslog_ike', 'syslog_imc',
        'syslog_imv', 'syslog_job', 'syslog_knl', 'syslog_lib', 'syslog_mgr', 'syslog_net', 'syslog_pts',
        'syslog_tls', 'syslog_tnc', 'attr_subnet', 'attr_dns', 'attr_nbns', 'unity_split_include',
        'unity_dns_search', 'unity_dns_split', 'unity_login_banner', 'unity_save_password',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'prefer_old_sa': ('general', 'preferred_oldsa'),
        'disable_vpn_rules': ('general', 'disablevpnrules'),
        'passthrough_networks': ('general', 'passthrough_networks'),
        'authentication': ('general', 'user_source'),
        'local_group': ('general', 'local_group'),
        'radius_servers': ('charon', 'plugins', 'eap-radius', 'servers'),
        'radius_accounting': ('charon', 'plugins', 'eap-radius', 'accounting'),
        'radius_class_group': ('charon', 'plugins', 'eap-radius', 'class_group'),
        'pam_service': ('charon', 'plugins', 'xauth-pam', 'pam_service'),
        'pam_session': ('charon', 'plugins', 'xauth-pam', 'session'),
        'pam_trim_email': ('charon', 'plugins', 'xauth-pam', 'trim_email'),
        'charon_max_ikev1_exchanges': ('charon', 'max_ikev1_exchanges'),
        'charon_threads': ('charon', 'threads'),
        'charon_ikesa_table_size': ('charon', 'ikesa_table_size'),
        'charon_ikesa_table_segments': ('charon', 'ikesa_table_segments'),
        'charon_init_limit_half_open': ('charon', 'init_limit_half_open'),
        'charon_ignore_acquire_ts': ('charon', 'ignore_acquire_ts'),
        'charon_make_before_break': ('charon', 'make_before_break'),
        'charon_install_routes': ('charon', 'install_routes'),
        'charon_cisco_unity': ('charon', 'cisco_unity'),
        'retransmit_tries': ('charon', 'retransmit_tries'),
        'retransmit_timeout': ('charon', 'retransmit_timeout'),
        'retransmit_base': ('charon', 'retransmit_base'),
        'retransmit_jitter': ('charon', 'retransmit_jitter'),
        'retransmit_limit': ('charon', 'retransmit_limit'),
        'syslog_log_name': ('charon', 'syslog', 'daemon', 'ike_name'),
        'syslog_log_level': ('charon', 'syslog', 'daemon', 'log_level'),
        'syslog_app': ('charon', 'syslog', 'daemon', 'app'),
        'syslog_asn': ('charon', 'syslog', 'daemon', 'asn'),
        'syslog_cfg': ('charon', 'syslog', 'daemon', 'cfg'),
        'syslog_chd': ('charon', 'syslog', 'daemon', 'app'),
        'syslog_dmn': ('charon', 'syslog', 'daemon', 'dmn'),
        'syslog_enc': ('charon', 'syslog', 'daemon', 'enc'),
        'syslog_esp': ('charon', 'syslog', 'daemon', 'esp'),
        'syslog_ike': ('charon', 'syslog', 'daemon', 'ike'),
        'syslog_imc': ('charon', 'syslog', 'daemon', 'imc'),
        'syslog_imv': ('charon', 'syslog', 'daemon', 'imv'),
        'syslog_job': ('charon', 'syslog', 'daemon', 'job'),
        'syslog_knl': ('charon', 'syslog', 'daemon', 'app'),
        'syslog_lib': ('charon', 'syslog', 'daemon', 'knl'),
        'syslog_mgr': ('charon', 'syslog', 'daemon', 'mgr'),
        'syslog_net': ('charon', 'syslog', 'daemon', 'net'),
        'syslog_pts': ('charon', 'syslog', 'daemon', 'pts'),
        'syslog_tls': ('charon', 'syslog', 'daemon', 'tls'),
        'syslog_tnc': ('charon', 'syslog', 'daemon', 'tnc'),
        'attr_subnet': ('charon', 'plugins', 'attr', 'subnet'),
        'attr_dns': ('charon', 'plugins', 'attr', 'dns'),
        'attr_nbns': ('charon', 'plugins', 'attr', 'nbns'),
        'unity_split_include': ('charon', 'plugins', 'attr', 'split-include'),
        'unity_dns_search': ('charon', 'plugins', 'attr', 'x_28674'),
        'unity_dns_split': ('charon', 'plugins', 'attr', 'x_28675'),
        'unity_login_banner': ('charon', 'plugins', 'attr', 'x_28672'),
        'unity_save_password': ('charon', 'plugins', 'attr', 'x_28673'),
    }
    FIELDS_TYPING = {
        'bool': [
            'prefer_old_sa', 'disable_vpn_rules', 'radius_accounting', 'radius_class_group', 'pam_session',
            'pam_trim_email', 'charon_ignore_acquire_ts', 'charon_make_before_break', 'charon_install_routes',
            'charon_cisco_unity', 'syslog_log_name', 'syslog_log_level', 'unity_save_password',
        ],
        'int': [
            'charon_max_ikev1_exchanges', 'charon_threads', 'charon_ikesa_table_size', 'charon_ikesa_table_segments',
            'charon_init_limit_half_open', 'retransmit_tries', 'retransmit_timeout', 'retransmit_base',
            'retransmit_jitter', 'retransmit_limit',
        ],
        'list': [
            'passthrough_networks', 'authentication', 'radius_servers', 'attr_subnet', 'attr_dns', 'attr_nbns',
            'unity_split_include',
        ],
        'select': [
            'local_group', 'syslog_app', 'syslog_asn', 'syslog_cfg', 'syslog_chd', 'syslog_dmn', 'syslog_enc',
            'syslog_esp', 'syslog_ike', 'syslog_imc', 'syslog_imv', 'syslog_job', 'syslog_knl', 'syslog_lib',
            'syslog_mgr', 'syslog_net', 'syslog_pts', 'syslog_tls', 'syslog_tnc',
        ],
    }
    INT_VALIDATIONS = {
        'charon_threads': {'min': 1, 'max': 65536},
        'charon_ikesa_table_size': {'min': 1, 'max': 65536},
        'charon_ikesa_table_segments': {'min': 1, 'max': 65536},
        'charon_init_limit_half_open': {'min': 1, 'max': 65536},
    }
    SEARCH_ADDITIONAL = {
        'existing_groups': 'ipsec.general.local_group',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
        self.existing_groups = {}

    def check(self) -> None:
        self._base_check()
        self.find_single_link(
            field='local_group',
            existing=self.existing_groups,
            existing_field_id='value',
        )
