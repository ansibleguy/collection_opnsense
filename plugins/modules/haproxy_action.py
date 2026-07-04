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
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_action import HaproxyAction

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name to identify this rule'
        ),
        description=dict(
            type='str', required=False, default='',
            description='Description for this rule'
        ),
        test_type=dict(
            type='str', required=False, default=None,
            choices=['if', 'unless'],
            description='Choose how to test the condition'
        ),
        linked_acls=dict(
            type='list', required=False, default=None,
            description='Select one or more conditions to be used for this rule'
        ),
        operator=dict(
            type='str', required=False, default=None,
            choices=['and', 'or'],
            description='Choose a logical operator to combine conditions'
        ),
        kind=dict(
            type='str', required=False, default=None, aliases=['type'],
            choices=[
                'compression', 'fcgi_pass_header', 'fcgi_set_param', 'http-after-response',
                'http-request', 'http-response', 'map_data_use_backend', 'map_use_backend',
                'monitor_fail', 'tcp-request', 'tcp-response', 'use_backend', 'use_server', 'custom',
            ],
            description='Select HAProxy action type to execute when condition matches'
        ),
        use_backend=dict(
            type='str', required=False, default='',
            description='HAProxy will use this backend pool if the condition evaluates to true'
        ),
        use_server=dict(
            type='str', required=False, default='',
            description='HAProxy will use this server instead of other servers'
        ),
        custom_rule=dict(
            type='str', required=False, default='',
            description='Custom rule (option pass-through)'
        ),
        fcgi_pass_header=dict(type='str', required=False, default=''),
        fcgi_set_param=dict(type='str', required=False, default=''),
        monitor_fail_uri=dict(type='str', required=False, default=''),

        # HTTP After Response
        http_after_response_action=dict(
            type='str', required=False, default=None,
            choices=['add-header', 'allow', 'capture', 'del-header', 'del-map', 'do-log', 'replace-header',
                     'replace-value', 'sc-add-gpc', 'sc-inc-gpc', 'sc-inc-gpc0', 'sc-inc-gpc1', 'sc-set-gpt',
                     'sc-set-gpt0', 'set-header', 'set-log-level', 'set-map', 'set-status', 'set-var', 'set-var-fmt',
                     'strict-mode', 'unset-var']
        ),
        http_after_response_option=dict(type='str', required=False, default=''),

        # HTTP Request fields
        http_request_action=dict(
            type='str', required=False, default=None,
            choices=['add-acl', 'add-header', 'allow', 'auth', 'cache-use', 'capture', 'del-acl', 'del-header',
                     'del-map', 'deny', 'disable-l7-retry', 'do-log', 'do-resolve', 'early-hint', 'lua',
                     'normalize-uri', 'redirect', 'reject', 'replace-header', 'replace-path', 'replace-pathq',
                     'replace-uri', 'replace-value', 'return', 'sc-add-gpc', 'sc-inc-gpc', 'sc-inc-gpc0', 'sc-inc-gpc1',
                     'sc-set-gpt', 'sc-set-gpt0', 'send-spoe-group', 'set-dst', 'set-dst-port', 'set-fc-mark',
                     'set-fc-tos', 'set-header', 'set-log-level', 'set-map', 'set-method', 'set-nice', 'set-path',
                     'set-pathq', 'set-priority-class', 'set-priority-offset', 'set-query', 'set-src', 'set-src-port',
                     'set-timeout', 'set-uri', 'set-var', 'set-var-fmt', 'silent-drop', 'strict-mode', 'tarpit',
                     'track-sc0', 'track-sc1', 'track-sc2', 'unset-var', 'use-service', 'wait-for-body',
                     'wait-for-handshake']
        ),
        http_request_option=dict(type='str', required=False, default=''),
        http_request_auth=dict(type='str', required=False, default=''),
        http_request_deny_status=dict(type='int', required=False),
        http_request_redirect=dict(type='str', required=False, default=''),
        http_request_lua=dict(type='str', required=False, default=''),
        http_request_use_service=dict(type='str', required=False, default=''),
        http_request_add_header_name=dict(type='str', required=False, default=''),
        http_request_add_header_content=dict(type='str', required=False, default=''),
        http_request_set_header_name=dict(type='str', required=False, default=''),
        http_request_set_header_content=dict(type='str', required=False, default=''),
        http_request_del_header_name=dict(type='str', required=False, default=''),
        http_request_replace_header_name=dict(type='str', required=False, default=''),
        http_request_replace_header_regex=dict(type='str', required=False, default=''),
        http_request_replace_value_name=dict(type='str', required=False, default=''),
        http_request_replace_value_regex=dict(type='str', required=False, default=''),
        http_request_set_path=dict(type='str', required=False, default=''),
        http_request_set_var_scope=dict(
            type='str', required=False, default=None,
            choices=['proc', 'sess', 'txn', 'req', 'res']
        ),
        http_request_set_var_name=dict(type='str', required=False, default=''),
        http_request_set_var_expr=dict(type='str', required=False, default=''),

        # HTTP Response fields
        http_response_action=dict(
            type='str', required=False, default=None,
            choices=['add-acl', 'add-header', 'allow', 'cache-store', 'capture', 'del-acl', 'del-header', 'del-map',
                     'deny', 'do-log', 'lua', 'redirect', 'replace-header', 'replace-value', 'return', 'sc-add-gpc',
                     'sc-inc-gpc', 'sc-inc-gpc0', 'sc-inc-gpc1', 'sc-set-gpt', 'sc-set-gpt0', 'send-spoe-group',
                     'set-fc-mark', 'set-fc-tos', 'set-header', 'set-log-level', 'set-map', 'set-nice', 'set-status',
                     'set-timeout', 'set-var', 'set-var-fmt', 'silent-drop', 'strict-mode', 'track-sc0', 'track-sc1',
                     'track-sc2', 'unset-var', 'wait-for-body']
        ),
        http_response_option=dict(type='str', required=False, default=''),
        http_response_lua=dict(type='str', required=False, default=''),
        http_response_add_header_name=dict(type='str', required=False, default=''),
        http_response_add_header_content=dict(type='str', required=False, default=''),
        http_response_set_header_name=dict(type='str', required=False, default=''),
        http_response_set_header_content=dict(type='str', required=False, default=''),
        http_response_del_header_name=dict(type='str', required=False, default=''),
        http_response_replace_header_name=dict(type='str', required=False, default=''),
        http_response_replace_header_regex=dict(type='str', required=False, default=''),
        http_response_replace_value_name=dict(type='str', required=False, default=''),
        http_response_replace_value_regex=dict(type='str', required=False, default=''),
        http_response_set_status_code=dict(type='int', required=False),
        http_response_set_status_reason=dict(type='str', required=False, default=''),
        http_response_set_var_scope=dict(
            type='str', required=False, default=None,
            choices=['proc', 'sess', 'txn', 'req', 'res']
        ),
        http_response_set_var_name=dict(type='str', required=False, default=''),
        http_response_set_var_expr=dict(type='str', required=False, default=''),

        # TCP fields
        tcp_request_action=dict(
            type='str', required=False, default=None,
            choices=['connection_accept', 'connection_expect-netscaler-cip', 'connection_expect-proxy',
                     'connection_fc-silent-drop', 'connection_reject', 'connection_sc-add-gpc', 'connection_sc-inc-gpc',
                     'connection_sc-inc-gpc0', 'connection_sc-inc-gpc1', 'connection_sc-set-gpt',
                     'connection_sc-set-gpt0', 'connection_send-spoe-group', 'connection_set-dst',
                     'connection_set-dst-port', 'connection_set-fc-mark', 'connection_set-fc-tos',
                     'connection_set-log-level', 'connection_set-src', 'connection_set-src-port', 'connection_set-var',
                     'connection_set-var-fmt', 'connection_silent-drop', 'connection_track-sc0', 'connection_track-sc1',
                     'connection_track-sc2', 'connection_unset-var', 'content_accept', 'content_capture',
                     'content_do-resolve', 'content_lua', 'content_reject', 'content_sc-add-gpc', 'content_sc-inc-gpc',
                     'content_sc-inc-gpc0', 'content_sc-inc-gpc1', 'content_sc-set-gpt', 'content_sc-set-gpt0',
                     'content_send-spoe-group', 'content_set-dst', 'content_set-dst-port', 'content_set-fc-mark',
                     'content_set-fc-tos', 'content_set-log-level', 'content_set-nice', 'content_set-priority-class',
                     'content_set-priority-offset', 'content_set-src', 'content_set-src-port', 'content_set-var',
                     'content_set-var-fmt', 'content_silent-drop', 'content_switch-mode', 'content_track-sc0',
                     'content_track-sc1', 'content_track-sc2', 'content_unset-var', 'content_use-service',
                     'inspect-delay', 'session_accept', 'session_attach-srv', 'session_reject', 'session_sc-add-gpc',
                     'session_sc-inc-gpc', 'session_sc-inc-gpc0', 'session_sc-inc-gpc1', 'session_sc-set-gpt',
                     'session_sc-set-gpt0', 'session_send-spoe-group', 'session_set-dst', 'session_set-dst-port',
                     'session_set-fc-mark', 'session_set-fc-tos', 'session_set-log-level', 'session_set-src',
                     'session_set-src-port', 'session_set-var', 'session_set-var-fmt', 'session_silent-drop',
                     'session_track-sc0', 'session_track-sc1', 'session_track-sc2', 'session_unset-var']
        ),
        tcp_request_option=dict(type='str', required=False, default=''),
        tcp_request_content_lua=dict(type='str', required=False, default=''),
        tcp_request_content_use_service=dict(type='str', required=False, default=''),
        tcp_request_inspect_delay=dict(type='str', required=False, default=''),

        tcp_response_action=dict(
            type='str', required=False, default=None,
            choices=['content_accept', 'content_close', 'content_lua', 'content_reject', 'content_sc-add-gpc',
                     'content_sc-inc-gpc', 'content_sc-inc-gpc0', 'content_sc-inc-gpc1', 'content_sc-set-gpt',
                     'content_sc-set-gpt0', 'content_send-spoe-group', 'content_set-fc-mark', 'content_set-fc-tos',
                     'content_set-log-level', 'content_set-nice', 'content_set-var', 'content_set-var-fmt',
                     'content_silent-drop', 'content_unset-var', 'inspect-delay']
        ),
        tcp_response_option=dict(type='str', required=False, default=''),
        tcp_response_content_lua=dict(type='str', required=False, default=''),
        tcp_response_inspect_delay=dict(type='str', required=False, default=''),

        # Map use backend
        map_data_use_backend_file=dict(type='str', required=False, default=''),
        map_data_use_backend_default=dict(type='str', required=False, default=''),
        map_data_use_backend_input=dict(type='str', required=False, default=''),
        map_use_backend_file=dict(type='str', required=False, default=''),
        map_use_backend_default=dict(type='str', required=False, default=''),

        # Compression
        compression_algo_res=dict(type='str', required=False, default=None, choices=['gzip', 'deflate', 'raw-deflate']),
        compression_algo_req=dict(type='str', required=False, default=None, choices=['gzip', 'deflate', 'raw-deflate']),
        compression_mime_res=dict(type='list', elements='str', required=False, default=[]),
        compression_mime_req=dict(type='list', elements='str', required=False, default=[]),
        compression_offloading=dict(type='bool', required=False, default=False),
        compression_minsize_res=dict(type='int', required=False),
        compression_minsize_req=dict(type='int', required=False),
        compression_direction=dict(type='str', required=False, default=None, choices=['response', 'request', 'both']),

        # Others
        gpc_number=dict(type='int', required=False),
        gpt_number=dict(type='int', required=False),
        sc_number=dict(type='int', required=False),
        mapfile=dict(type='str', required=False, default=''),
        map_default=dict(type='str', required=False, default=''),
        sample_fetch=dict(type='str', required=False, default=''),

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
    )

    module_wrapper(HaproxyAction(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
