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
        OPN_MOD_ARGS, RELOAD_MOD_ARG, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_remote_acl import Acl

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'


def run_module():
    module_args = dict(
        file=dict(
            type='str', required=True, aliases=['filename'],
            description='Unique file-name to store the remote acl in'
        ),
        url=dict(
            type='str', required=False, default='',
            description='Url to fetch the acl from'
        ),
        username=dict(
            type='str', required=False, default='', aliases=['user'],
            description='Optional user for authentication'
        ),
        password=dict(
            type='str', required=False, default='', aliases=['pwd'],
            description='Optional password for authentication',
            no_log=True,
        ),
        categories=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['cat', 'filter'],
            description='Select categories to use, leave empty for all. '
                        'Categories are visible in the WEB-UI after initial download'
        ),
        verify_ssl=dict(
            type='bool', required=False, default=True, aliases=['verify'],
            description='If certificate validation should be done - relevant if '
                        'self-signed certificates are used on the target server!'
        ),
        description=dict(
            type='str', required=False, default='', aliases=['desc'],
            description='A description to explain what this blacklist is intended for'
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
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

    module_wrapper(Acl(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
