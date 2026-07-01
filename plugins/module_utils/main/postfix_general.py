from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'general'
    API_MOD = 'postfix'
    API_CONT = 'general'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'myhostname', 'mydomain', 'myorigin', 'inet_interfaces', 'inet_port', 'ip_version', 'bind_address',
        'bind_address6', 'mynetworks', 'banner', 'message_size_limit', 'masquerade_domains',
        'tls_server_compatibility', 'tls_client_compatibility', 'certificate', 'ca', 'smtpclient_security',
        'relayhost', 'smtpauth_enabled', 'smtpauth_user', 'smtpauth_password', 'enforce_recipient_check',
        'extensive_helo_restrictions', 'extensive_sender_restrictions', 'reject_unknown_client_hostname',
        'reject_non_fqdn_helo_hostname', 'reject_invalid_helo_hostname', 'reject_unknown_helo_hostname',
        'reject_unauth_pipelining', 'reject_unknown_sender_domain', 'reject_unknown_recipient_domain',
        'reject_non_fqdn_sender', 'reject_non_fqdn_recipient', 'permit_sasl_authenticated', 'permit_tls_clientcerts',
        'permit_mynetworks', 'reject_unauth_destination', 'reject_unverified_recipient', 'delay_warning_time',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'tlswrappermode', 'smtpauth_enabled', 'enforce_recipient_check', 'extensive_helo_restrictions',
            'extensive_sender_restrictions', 'reject_unknown_client_hostname', 'reject_non_fqdn_helo_hostname',
            'reject_invalid_helo_hostname', 'reject_unknown_helo_hostname', 'reject_unauth_pipelining',
            'reject_unknown_sender_domain', 'reject_unknown_recipient_domain', 'reject_non_fqdn_sender',
            'reject_non_fqdn_recipient', 'permit_sasl_authenticated', 'permit_tls_clientcerts', 'permit_mynetworks',
            'reject_unauth_destination', 'reject_unverified_recipient',
        ],
        'list': ['inet_interfaces', 'mynetworks', 'masquerade_domains'],
        'select': [
            'ip_version', 'tls_server_compatibility', 'tls_client_compatibility', 'certificate', 'ca',
            'smtpclient_security',
        ],
        'int': ['inet_port', 'message_size_limit', 'delay_warning_time'],
    }
    INT_VALIDATIONS = {
        'inet_port': {'min': 1, 'max': 65535},
        'delay_warning_time': {'min': 0, 'max': 24},
    }
    EXIST_ATTR = 'settings'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
