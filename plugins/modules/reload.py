#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to reload running config
# pylint: disable=R0912,R0915,R0914

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()


DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/reload.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/modules/reload.html'


def run_module():
    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['tgt', 't'],
            choises=[
                'alias', 'route', 'cron', 'unbound', 'syslog', 'ipsec', 'shaper',
                'monit', 'wireguard', 'interface_vlan', 'interface_vxlan', 'frr',
                'webproxy',
            ],
            description='What part of the running config should be reloaded'
        ),
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    target = None

    try:
        # todo: refactor to use config-dict and dynamic imports

        if module.params['target'] == 'alias':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.alias import Alias
            target = Alias(module=module, result=result)

        elif module.params['target'] == 'rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule import Rule
            target = Rule(module=module, result=result)

        elif module.params['target'] == 'route':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.route import Route
            target = Route(module=module, result=result)

        elif module.params['target'] == 'cron':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.cron import CronJob
            target = CronJob(module=module, result=result)

        elif module.params['target'] == 'unbound':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_host import Host
            target = Host(module=module, result=result)

        elif module.params['target'] == 'syslog':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.syslog import Syslog
            target = Syslog(module=module, result=result)

        elif module.params['target'] == 'ipsec':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_cert import KeyPair
            target = KeyPair(module=module, result=result)

        elif module.params['target'] == 'shaper':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_pipe import Pipe
            target = Pipe(module=module, result=result)

        elif module.params['target'] == 'monit':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_service import Service
            target = Service(module=module, result=result)

        elif module.params['target'] == 'wireguard':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wireguard_server import Server
            target = Server(module=module, result=result)

        elif module.params['target'] == 'interface_vlan':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vlan import Vlan
            target = Vlan(module=module, result=result)

        elif module.params['target'] == 'interface_vxlan':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vxlan import Vxlan
            target = Vxlan(module=module, result=result)

        elif module.params['target'] == 'frr':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_general import General
            target = General(module=module, result=result)

        elif module.params['target'] == 'webproxy':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_general import General
            target = General(module=module, result=result)

    except MODULE_EXCEPTIONS:
        module_dependency_error()

    if target is not None:
        result['changed'] = True
        if not module.check_mode:
            target.reload()

        if hasattr(target, 's'):
            target.s.close()

    else:
        module.fail_json(f"Got unsupported target: '{module.params['target']}'")

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
