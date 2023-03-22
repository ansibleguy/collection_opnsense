#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_network import Network

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_bgp.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_bgp.html'


def run_module():
    module_args = dict(
        ip=dict(type='str', required=True, aliases=['nw_address', 'network_address', 'address']),
        mask=dict(type='int', required=True, aliases=['nw_mask', 'network_mask']),
        area=dict(
            type='str', required=False, default='',
            description='Area in wildcard mask style like 0.0.0.0 and no decimal 0. '
                        'Only use Area in Interface tab or in Network tab once'
        ),
        area_range=dict(
            type='str', required=False, default='',
            description='Here you can summarize a network for this area like 192.168.0.0/23'
        ),
        prefix_list_in=dict(
            type='str', required=False, default='', aliases=['prefix_in', 'pre_in']
        ),
        prefix_list_out=dict(
            type='str', required=False, default='', aliases=['prefix_out', 'pre_out']
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured network with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['ip', 'mask', 'area', 'area_range'],
            default=['ip', 'mask'],
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

    nw = Network(module=module, result=result)

    def process():
        nw.check()
        nw.process()
        if result['changed'] and module.params['reload']:
            nw.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='frr_ospf_network.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    nw.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
