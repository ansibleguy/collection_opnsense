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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_community_list import Community

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-community-list'
EXAMPLES = 'https://opnsense.ansibleguy.net/modules/frr_bgp.html#id5'


def run_module():
    module_args = dict(
        description=dict(type='str', required=True, aliases=['desc']),
        number=dict(type='str', required=False, aliases=['nr']),
        seq=dict(type='str', required=False, default='', aliases=['seq_number']),
        action=dict(type='str', required=False, default='', options=['permit', 'deny']),
        community=dict(
            type='str', required=False, default='', aliases=['comm'],
            description='The community you want to match. You can also regex and it is '
                        'not validated so please be careful.'
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

    community = Community(module=module, result=result)

    def process():
        community.check()
        community.process()
        if result['changed'] and module.params['reload']:
            community.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='frr_bgp_community_list.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    community.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
