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
            description='Choose how to test the condition. IF [default] tests if condition is true, '
                        'UNLESS tests if condition is false'
        ),
        linked_acls=dict(
            type='list', required=False, default=None,
            description='Select one or more conditions to be used for this rule'
        ),
        operator=dict(
            type='str', required=False, default=None,
            choices=['and', 'or'],
            description='Choose a logical operator to combine conditions: AND [default] or OR'
        ),
        kind=dict(
            type='str', required=False, default=None, aliases=['type'],
            choices=['use_backend', 'use_server', 'map_use_backend', 'fcgi_pass_header', 'fcgi_set_param',
                     'http-request_allow', 'http-request_deny', 'http-request_tarpit', 'http-request_auth',
                     'http-request_redirect', 'http-request_lua', 'http-request_use-service',
                     'http-request_add-header', 'http-request_set-header', 'http-request_del-header',
                     'http-request_replace-header', 'http-request_replace-value', 'http-request_set-path',
                     'http-request_set-var', 'http-response_allow', 'http-response_deny', 'http-response_lua',
                     'http-request', 'http-response_add-header', 'http-response_set-header', 'http-response_del-header',
                     'http-response_replace-header', 'http-response_replace-value', 'http-response_set-status',
                     'http-response_set-var', 'monitor_fail', 'tcp-request_connection_accept',
                     'tcp-request_connection_reject', 'tcp-request_content_accept', 'tcp-request_content_reject',
                     'tcp-request_content_lua', 'tcp-request_content_use-service', 'tcp-request_inspect-delay',
                     'tcp-response_content_accept', 'tcp-response_content_close', 'tcp-response_content_reject',
                     'tcp-response_content_lua', 'tcp-response_inspect-delay', 'custom'],
            description='Select HAProxy action type to execute when condition matches'
        ),
        use_backend=dict(
            type='str', required=False, default='',
            description='HAProxy will use this backend pool if the condition evaluates to true'
        ),
        use_server=dict(
            type='str', required=False, default='',
            description='HAProxy will use this server instead of other servers that are specified in the Backend Pool'
        ),
        custom_rule=dict(
            type='str', required=False, default='',
            description='Custom rule (option pass-through)'
        ),
        # FastCGI fields
        fcgi_pass_header=dict(
            type='str', required=False, default='',
            description='FastCGI pass-header'
        ),
        fcgi_set_param=dict(
            type='str', required=False, default='',
            description='FastCGI set-param'
        ),
        # HTTP Request fields
        http_request_auth=dict(
            type='str', required=False, default='',
            description='HTTP request auth realm'
        ),
        http_request_redirect=dict(
            type='str', required=False, default='',
            description='HTTP request redirect location'
        ),
        http_request_lua=dict(
            type='str', required=False, default='',
            description='HTTP request lua action'
        ),
        http_request_use_service=dict(
            type='str', required=False, default='',
            description='HTTP request lua service'
        ),
        # HTTP Request Header Add
        http_request_add_header_name=dict(
            type='str', required=False, default='',
            description='HTTP request header name to add'
        ),
        http_request_add_header_content=dict(
            type='str', required=False, default='',
            description='HTTP request header content to add'
        ),
        # HTTP Request Header Set
        http_request_set_header_name=dict(
            type='str', required=False, default='',
            description='HTTP request header name to set'
        ),
        http_request_set_header_content=dict(
            type='str', required=False, default='',
            description='HTTP request header content to set'
        ),
        # HTTP Request Header Delete
        http_request_del_header_name=dict(
            type='str', required=False, default='',
            description='HTTP request header name to delete'
        ),
        # HTTP Request Header Replace
        http_request_replace_header_name=dict(
            type='str', required=False, default='',
            description='HTTP request header name to replace'
        ),
        http_request_replace_header_regex=dict(
            type='str', required=False, default='',
            description='HTTP request header regex to replace'
        ),
        http_request_replace_value_name=dict(
            type='str', required=False, default='',
            description='HTTP request value name to replace'
        ),
        http_request_replace_value_regex=dict(
            type='str', required=False, default='',
            description='HTTP request value regex to replace'
        ),
        # HTTP Request Set Path
        http_request_set_path=dict(
            type='str', required=False, default='',
            description='HTTP request set-path value'
        ),
        # HTTP Request Set Variable
        http_request_set_var_scope=dict(
            type='str', required=False, default=None,
            choices=['proc', 'sess', 'txn', 'req', 'res'],
            description='Variable scope: proc (whole process), sess (whole session), txn (transaction), '
            'req (request only), res (response only)'
        ),
        http_request_set_var_name=dict(
            type='str', required=False, default='',
            description='HTTP request set-var name'
        ),
        http_request_set_var_expr=dict(
            type='str', required=False, default='',
            description='HTTP request set-var expression'
        ),
        # HTTP Response fields
        http_response_lua=dict(
            type='str', required=False, default='',
            description='HTTP response lua script'
        ),
        # HTTP Response Header Add
        http_response_add_header_name=dict(
            type='str', required=False, default='',
            description='HTTP response header name to add'
        ),
        http_response_add_header_content=dict(
            type='str', required=False, default='',
            description='HTTP response header content to add'
        ),
        # HTTP Response Header Set
        http_response_set_header_name=dict(
            type='str', required=False, default='',
            description='HTTP response header name to set'
        ),
        http_response_set_header_content=dict(
            type='str', required=False, default='',
            description='HTTP response header content to set'
        ),
        # HTTP Response Header Delete
        http_response_del_header_name=dict(
            type='str', required=False, default='',
            description='HTTP response header name to delete'
        ),
        # HTTP Response Header Replace
        http_response_replace_header_name=dict(
            type='str', required=False, default='',
            description='HTTP response header name to replace'
        ),
        http_response_replace_header_regex=dict(
            type='str', required=False, default='',
            description='HTTP response header regex to replace'
        ),
        http_response_replace_value_name=dict(
            type='str', required=False, default='',
            description='HTTP response value name to replace'
        ),
        http_response_replace_value_regex=dict(
            type='str', required=False, default='',
            description='HTTP response value regex to replace'
        ),
        http_response_set_status_code=dict(
            type='int', required=False,
            description='HTTP response status code (100-999)'
        ),
        http_response_set_status_reason=dict(
            type='str', required=False, default='',
            description='HTTP response status reason'
        ),
        # HTTP Response Set Variable
        http_response_set_var_scope=dict(
            type='str', required=False, default=None,
            choices=['proc', 'sess', 'txn', 'req', 'res'],
            description='Variable scope: proc (whole process), sess (whole session), txn (transaction), '
            'req (request only), res (response only)'
        ),
        http_response_set_var_name=dict(
            type='str', required=False, default='',
            description='HTTP response set-var name'
        ),
        http_response_set_var_expr=dict(
            type='str', required=False, default='',
            description='HTTP response set-var expression'
        ),
        # TCP fields
        tcp_request_content_lua=dict(
            type='str', required=False, default='',
            description='TCP request content lua script'
        ),
        tcp_request_content_use_service=dict(
            type='str', required=False, default='',
            description='TCP request content use-service'
        ),
        tcp_request_inspect_delay=dict(
            type='str', required=False, default='',
            description='TCP request inspect-delay'
        ),
        tcp_response_content_lua=dict(
            type='str', required=False, default='',
            description='TCP response content lua script'
        ),
        tcp_response_inspect_delay=dict(
            type='str', required=False, default='',
            description='TCP response inspect-delay'
        ),
        # Monitor fail
        monitor_fail_uri=dict(
            type='str', required=False, default='',
            description='Monitor fail URI'
        ),
        # Map use backend
        map_use_backend_file=dict(
            type='str', required=False, default='',
            description='Map file for backend selection'
        ),
        map_use_backend_default=dict(
            type='str', required=False, default='',
            description='Default backend for map-based selection'
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
    )

    module_wrapper(HaproxyAction(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
