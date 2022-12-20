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
        OPN_MOD_ARGS, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bfd_neighbor import Neighbor

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/frr_bfd.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/modules/frr_bfd.html'


def run_module():
    module_args = dict(
        ip=dict(type='str', required=True, aliases=[
            'neighbor', 'peer', 'peer_ip', 'address',
        ]),
        description=dict(type='str', required=False, default='', aliases=['desc']),
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

    neighbor = Neighbor(module=module, result=result)

    def process():
        neighbor.check()
        neighbor.process()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='frr_bfd_neighbor.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    neighbor.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
