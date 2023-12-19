#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'

BLANK_VALUES = {
    'errors': 'squid',
    'log_target': 'file',
    'handling_forwarded_for': 'default',
}


def run_module():
    module_args = dict(
        errors=dict(
            type='str', required=False, default='opnsense', aliases=['error_pages'],
            choices=['opnsense', 'custom', 'squid'],
            description='The proxy error pages can be altered, default layout uses '
                        'OPNsense content, when Squid is selected the content for the '
                        'selected language will be used (standard squid layout), Custom '
                        'offers the possibility to upload your own theme content'
        ),
        icp_port=dict(type='str', required=False, default='', aliases=['icp']),
        log=dict(type='bool', required=False, default=True),
        log_store=dict(type='bool', required=False, default=True),
        log_target=dict(
            type='str', required=False, default='file',
            choices=['file', 'file_extendend', 'file_json', 'syslog', 'syslog_json'],
            description='Send log data to the selected target. When syslog is selected, '
                        'facility local 4 will be used to send messages of info level for these logs'
        ),
        log_ignore=dict(
            type='list', elements='str', required=False, default=[],
            description='Type subnets/addresses you want to ignore for the access.log'
        ),
        dns_servers=dict(
            type='list', elements='str', required=False, default=[],
            description='IPs of alternative DNS servers you like to use'
        ),
        use_via_header=dict(
            type='bool', required=False, default=True,
            description='If set (default), Squid will include a Via header in requests and replies '
                        'as required by RFC2616'
        ),
        handling_forwarded_for=dict(
            type='str', required=False, default='default',
            aliases=['forwarded_for_handling', 'forwarded_for', 'handle_ff'],
            choices=['default', 'on', 'off', 'transparent', 'delete', 'truncate'],
            description="Select what to do with X-Forwarded-For header. If set to: 'on', Squid will "
                        "append your client's IP address in the HTTP requests it forwards. By default "
                        "it looks like X-Forwarded-For: 192.1.2.3; If set to: 'off', it will appear as "
                        "X-Forwarded-For: unknown; 'transparent', Squid will not alter the X-Forwarded-For "
                        "header in any way; If set to: 'delete', Squid will delete the entire "
                        "X-Forwarded-For header; If set to: 'truncate', Squid will remove all existing "
                        "X-Forwarded-For entries, and place the client IP as the sole entry"
        ),
        hostname=dict(
            type='str', required=False, default='', aliases=['visible_hostname'],
            description='The hostname to be displayed in proxy server error messages'
        ),
        email=dict(
            type='str', required=False, default='admin@localhost.local', aliases=['visible_email'],
            description='The email address displayed in error messages to the users'
        ),
        suppress_version=dict(
            type='bool', required=False, default=False,
            description='Suppress Squid version string info in HTTP headers and HTML error pages'
        ),
        connect_timeout=dict(
            type='str', required=False, default='',
            description='This can help you when having connection issues with IPv6 enabled servers. '
                        'Set a value in seconds (1-120s)'
        ),
        handling_uri_whitespace=dict(
            type='str', required=False, default='strip',
            aliases=['uri_whitespace_handling', 'uri_whitespace', 'handle_uw'],
            choices=['strip', 'deny', 'allow', 'encode', 'chop'],
            description='Select what to do with URI that contain whitespaces. The current Squid '
                        'implementation of encode and chop violates RFC2616 by not using a 301 '
                        'redirect after altering the URL'
        ),
        pinger=dict(
            type='bool', required=False, default=True,
            description='Toggles the Squid pinger service. '
                        'This service is used in the selection of the best parent proxy'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
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

    for field, value in BLANK_VALUES.items():
        if module.params[field] == value:
            module.params[field] = ''  # BlankDesc

    module_wrapper(General(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
