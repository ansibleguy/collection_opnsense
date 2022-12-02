#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty, sort_param_lists
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_rip import Rip

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_rip.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_rip.md'


def run_module():
    module_args = dict(
        version=dict(type='int', required=False, default=2, aliases=['v']),
        metric=dict(
            type='str', required=False, default='', aliases=['m', 'default_metric'],
            description='Set the default metric to a value between 1 and 16'
        ),
        passive_ints=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['passive_interfaces'],
            description='Select the interfaces, where no RIP packets should be sent to'
        ),
        networks=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['nets'],
            description='Enter your networks in CIDR notation'
        ),
        redistribute=dict(
            type='list', elements='str', required=False, default=[],
            options=['bgp', 'ospf', 'connected', 'kernel', 'static'],
            description='Select other routing sources, which should be '
                        'redistributed to the other nodes'
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

    sort_param_lists(module.params)
    rip = Rip(module=module, result=result)

    def process():
        rip.check()
        rip.process()
        if result['changed'] and module.params['reload']:
            rip.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='frr_rip.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    rip.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
