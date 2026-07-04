#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_frontend import HaproxyFrontend

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name to identify this Public Service.'
        ),
        description=dict(
            type='str', required=False, default=None,
            description='Description for this Public Service.'
        ),
        bind=dict(
            type='list', elements='str', required=True,
            description='Listen addresses (e.g. 127.0.0.1:8080 or www.example.com:443).'
        ),
        bind_options=dict(
            type='str', required=False, default=None,
            description='A list of parameters that will be appended to every Listen Address line.'
        ),
        mode=dict(
            type='str', required=False, default='http',
            choices=['http', 'ssl', 'tcp'],
            description='Set the running mode or protocol for this Public Service.'
        ),
        default_backend=dict(
            type='str', required=False, default=None,
            description='Set the default Backend Pool to use for this Public Service.'
        ),
        ssl_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable SSL offloading.'
        ),
        ssl_certificates=dict(
            type='list', elements='str', required=False, default=[],
            description='Select certificates to use for SSL offloading.'
        ),
        ssl_default_certificate=dict(
            type='str', required=False, default=None,
            description='This certificate will be presented if no SNI is provided by the client.'
        ),
        ssl_custom_options=dict(
            type='str', required=False, default=None,
            description='Pass additional SSL parameters to the HAProxy configuration.'
        ),
        ssl_advanced_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable advanced SSL settings.'
        ),
        ssl_bind_options=dict(
            type='list', elements='str', required=False, default=['prefer-client-ciphers'],
            choices=[
                'no-sslv3', 'no-tlsv10', 'no-tlsv11', 'no-tlsv12', 'no-tlsv13',
                'no-tls-tickets', 'force-sslv3', 'force-tlsv10', 'force-tlsv11',
                'force-tlsv12', 'force-tlsv13', 'prefer-client-ciphers', 'strict-sni'
            ],
            description='SSL bind options for advanced SSL configuration.'
        ),
        ssl_min_version=dict(
            type='str', required=False, default=None,
            choices=['TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3'],
            description='This option enforces use of the specified version (or higher) on SSL connections.'
        ),
        ssl_max_version=dict(
            type='str', required=False, default=None,
            choices=['TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3'],
            description='This option enforces use of the specified version (or lower) on SSL connections.'
        ),
        ssl_cipher_list=dict(
            type='str', required=False, default=None,
            description='Set the list of allowed SSL cipher suites for SSLv3/TLSv1.0/TLSv1.1/TLSv1.2.'
        ),
        ssl_cipher_suites=dict(
            type='str', required=False, default=None,
            description='Set the list of allowed SSL cipher suites for TLSv1.3.'
        ),
        ssl_hsts_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable HTTP Strict Transport Security.'
        ),
        ssl_hsts_include_sub_domains=dict(
            type='bool', required=False, default=False,
            description='Include all subdomains in HSTS.'
        ),
        ssl_hsts_preload=dict(
            type='bool', required=False, default=False,
            description='Enable HSTS preload.'
        ),
        ssl_hsts_max_age=dict(
            type='int', required=False, default=15768000,
            description='Set max-age of the HSTS header in seconds.'
        ),
        ssl_client_auth_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable SSL client certificate authentication.'
        ),
        ssl_client_auth_verify=dict(
            type='str', required=False, default='required',
            choices=['none', 'optional', 'required'],
            description='Client certificate verification mode.'
        ),
        ssl_client_auth_cas=dict(
            type='list', elements='str', required=False, default=[],
            description='Certificate Authorities for client certificate verification.'
        ),
        ssl_client_auth_crls=dict(
            type='list', elements='str', required=False, default=[],
            description='Certificate Revocation Lists for client certificate verification.'
        ),
        http2_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable HTTP/2 support.'
        ),
        http2_enabled_nontls=dict(
            type='bool', required=False, default=False,
            description='Enable HTTP/2 even without TLS.'
        ),
        advertised_protocols=dict(
            type='list', elements='str', required=False, default=['h2', 'http11'],
            choices=['h3', 'h2', 'http11', 'http10'],
            description='Advertise these protocols via ALPN.'
        ),
        forwarded_header=dict(
            type='bool', required=False, default=False,
            description='Enable insertion of the RFC7239 forwarded header.'
        ),
        forward_for=dict(
            type='bool', required=False, default=False,
            description='Enable insertion of the X-Forwarded-For header.'
        ),
        basic_auth_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable HTTP Basic Authentication.'
        ),
        basic_auth_users=dict(
            type='list', elements='str', required=False, default=[],
            description='Allowed users for Basic Authentication.'
        ),
        basic_auth_groups=dict(
            type='list', elements='str', required=False, default=[],
            description='Allowed groups for Basic Authentication.'
        ),
        tuning_max_connections=dict(
            type='int', required=False, default=None,
            description='Set the maximum connections for this frontend.'
        ),
        tuning_timeout_client=dict(
            type='str', required=False, default=None,
            description='Set the maximum inactivity time on the client side.'
        ),
        tuning_timeout_http_req=dict(
            type='str', required=False, default=None,
            description='Set the maximum time to wait for a complete HTTP request.'
        ),
        tuning_timeout_http_keep_alive=dict(
            type='str', required=False, default=None,
            description='Set the maximum time for HTTP keep-alive timeout.'
        ),
        linked_cpu_affinity_rules=dict(
            type='list', elements='str', required=False, default=[],
            description='Select CPU affinity rules for this frontend.'
        ),
        tuning_shards=dict(
            type='int', required=False, default=None,
            description='Number of shards for this frontend.'
        ),
        logging_dont_log_null=dict(
            type='bool', required=False, default=False,
            description='Do not log connections with no data.'
        ),
        logging_dont_log_normal=dict(
            type='bool', required=False, default=False,
            description='Do not log normal connections.'
        ),
        logging_log_separate_errors=dict(
            type='bool', required=False, default=False,
            description='Log errors on a separate facility.'
        ),
        logging_detailed_log=dict(
            type='bool', required=False, default=False,
            description='Enable detailed logging.'
        ),
        logging_socket_stats=dict(
            type='bool', required=False, default=False,
            description='Enable socket statistics in logs.'
        ),
        stickiness_pattern=dict(
            type='str', required=False, default=None,
            choices=['binary', 'integer', 'ipv4', 'ipv6', 'string'],
            description='Pattern for stick table.'
        ),
        stickiness_data_types=dict(
            type='list', elements='str', required=False, default=[],
            description='Data types to store in the stick table.'
        ),
        stickiness_expire=dict(
            type='str', required=False, default='30m',
            description='Maximum duration of an entry in the stick table.'
        ),
        stickiness_size=dict(
            type='str', required=False, default='50k',
            description='Maximum number of entries in the stick table.'
        ),
        stickiness_counter=dict(
            type='bool', required=False, default=True,
            description='Enable stick table counters.'
        ),
        stickiness_counter_key=dict(
            type='str', required=False, default='src',
            description='Key for stick table counter.'
        ),
        stickiness_length=dict(
            type='int', required=False, default=None,
            description='Maximum length of strings in stick table.'
        ),
        stickiness_conn_rate_period=dict(
            type='str', required=False, default='10s',
            description='Period for connection rate tracking.'
        ),
        stickiness_sess_rate_period=dict(
            type='str', required=False, default='10s',
            description='Period for session rate tracking.'
        ),
        stickiness_http_req_rate_period=dict(
            type='str', required=False, default='10s',
            description='Period for HTTP request rate tracking.'
        ),
        stickiness_http_err_rate_period=dict(
            type='str', required=False, default='10s',
            description='Period for HTTP error rate tracking.'
        ),
        stickiness_bytes_in_rate_period=dict(
            type='str', required=False, default='1m',
            description='Period for bytes in rate tracking.'
        ),
        stickiness_bytes_out_rate_period=dict(
            type='str', required=False, default='1m',
            description='Period for bytes out rate tracking.'
        ),
        prometheus_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable Prometheus metrics endpoint.'
        ),
        prometheus_path=dict(
            type='str', required=False, default='/metrics',
            description='Path for Prometheus metrics endpoint.'
        ),
        connection_behaviour=dict(
            type='str', required=False, default='http-keep-alive',
            choices=['http-keep-alive', 'httpclose', 'http-server-close'],
            description='HTTP connection behavior.'
        ),
        custom_options=dict(
            type='str', required=False, default=None,
            description='These lines will be added to the HAProxy frontend configuration.'
        ),
        linked_actions=dict(
            type='list', elements='str', required=False, default=[],
            description='Choose rules to be included in this Public Service.'
        ),
        linked_errorfiles=dict(
            type='list', elements='str', required=False, default=[],
            description='Choose error messages to be included in this Public Service.'
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('ssl_enabled', True, ('ssl_certificates',)),
        ],
    )

    module_wrapper(HaproxyFrontend(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
