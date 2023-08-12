#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_acl import Acl

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/unbound.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/unbound.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['n'],
            decription='The access list name'
            ),
        action=dict(
            type='str', required=False, default='allow',
            choices=['allow', 'deny', 'refuse', 'allow_snoop', 'deny_non_local', 'refuse_non_local'],
            decription='What to to with DNS request that match the criteria'
        ),
        networks=dict(
            type='list', elements='str', required=False, aliases=['nets'],
            decription='The list of networks in CIDR notation to apply this ACL to'
        ),
        description=dict(
            type='str', required=False, default='', aliases=['desc'],
            decription='The description for the ACL'
        ),
        **STATE_MOD_ARG,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG,
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

    a = Acl(module=module, result=result)

    def process():
        a.check()
        a.process()
        if result['changed'] and module.params['reload']:
            a.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='unbound_acl.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    a.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
