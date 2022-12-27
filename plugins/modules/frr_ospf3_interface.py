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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf3_interface import Interface

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_ospf.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_ospf.html'


def run_module():
    module_args = dict(
        interface=dict(type='str', required=True, aliases=['name', 'int']),
        area=dict(
            type='str', required=False, default='',
            description='Area in wildcard mask style like 0.0.0.0 and no decimal 0'
        ),
        passive=dict(type='bool', required=False, default=False),
        cost=dict(type='str', required=False, default=''),
        cost_demoted=dict(type='int', required=False, default=65535),
        carp_depend_on=dict(
            type='str', required=False, default='',
            description='The carp VHID to depend on, when this virtual address is not in '
                        'master state, the interface cost will be set to the demoted cost'
        ),
        hello_interval=dict(type='str', required=False, default='', aliases=['hello']),
        dead_interval=dict(type='str', required=False, default='', aliases=['dead']),
        retransmit_interval=dict(type='str', required=False, default='', aliases=['retransmit']),
        transmit_delay=dict(type='str', required=False, default='', aliases=['delay']),
        priority=dict(type='str', required=False, default='', aliases=['prio']),
        network_type=dict(
            type='str', required=False, default='', aliases=['nw_type'],
            choises=['broadcast', 'point-to-point'],
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured interface with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choises=['interface', 'area', 'passive', 'carp_depend_on', 'network_type'],
            default=['interface', 'area'],
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

    interface = Interface(module=module, result=result)

    def process():
        interface.check()
        interface.process()
        if result['changed'] and module.params['reload']:
            interface.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='frr_ospf3_interface.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    interface.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
