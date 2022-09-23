#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/wireguard.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wireguard_peer import Peer

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md'


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        public_key=dict(type='str', required=False, alises=['pubkey', 'pub']),
        psk=dict(type='str', required=False, default=''),
        tunnel_ips=dict(
            type='list', elements='str', required=False, default=[],
            aliases=[
                'tunnel_ip', 'tunneladdress', 'tunnel_adresses', 'tunnel_address',
                'addresses', 'address',
            ]
        ),
        target=dict(
            type='str', required=False, default='',
            aliases=['endpoint', 'server_address', 'serveraddress', 'server']
        ),
        port=dict(type='str', required=False, default=''),
        keepalive=dict(type='str', required=False, default=''),
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

    peer = Peer(module=module, result=result)

    def process():
        peer.check()
        peer.process()
        if result['changed'] and module.params['reload']:
            peer.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='wireguard_peer.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    peer.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
