#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_as_path import AsPath

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md'


def run_module():
    module_args = dict(
        description=dict(type='str', required=True, aliases=['desc']),
        number=dict(
            type='str', required=False, aliases=['nr'],
            description='The ACL rule number (10-99); keep in mind that there are no '
                        'sequence numbers with AS-Path lists. When you want to add a '
                        'new line between you have to completely remove the ACL!'
        ),
        action=dict(type='str', required=False, default='', options=['permit', 'deny']),
        as_pattern=dict(
            type='str', required=False, default='', aliases=['as'],
            description="The AS pattern you want to match, regexp allowed (e.g. .$ or _1$). "
                        "It's not validated so please be careful!"
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

    as_path = AsPath(module=module, result=result)

    def process():
        as_path.check()
        as_path.process()
        if result['changed'] and module.params['reload']:
            as_path.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='frr_bgp_as_path.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    as_path.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
