#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/interfaces.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vxlan import Vxlan

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/interface.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/modules/interface.html'


def run_module():
    module_args = dict(
        # device_id=dict(type='str', required=True),  # can't be configured
        interface=dict(type='str', required=False, aliases=['vxlandev', 'device', 'int']),
        id=dict(type='int', required=True, aliases=['vxlanid', 'vni']),
        local=dict(
            type='str', required=False, aliases=[
                'source_address', 'source_ip', 'vxlanlocal', 'source', 'src',
            ],
            description='The source address used in the encapsulating IPv4/IPv6 header. The address should '
                        'already be assigned to an existing interface. When the interface is configured in '
                        'unicast mode, the listening socket is bound to this address.'
        ),
        remote=dict(
            type='str', required=False, aliases=[
                'remote_address', 'remote_ip', 'destination', 'vxlanremote', 'dest',
            ],
            description='The interface can be configured in a unicast, or point-to-point, mode to create '
                        'a tunnel between two hosts. This is the IP address of the remote end of the tunnel.'
        ),
        group=dict(
            type='str', required=False, aliases=[
                'multicast_group', 'multicast_address', 'multicast_ip', 'vxlangroup',
            ],
            description='The interface can be configured in a multicast mode to create a virtual '
                        'network of hosts. This is the IP multicast group address the interface will join.'
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
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

    vxlan = Vxlan(module=module, result=result)

    def process():
        vxlan.check()
        vxlan.process()
        if result['changed'] and module.params['reload']:
            vxlan.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='interface_vxlan.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    vxlan.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
