#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to reload running config

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()


DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md'


def run_module():
    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['dom', 'd'],
            choises=[
                'alias', 'route', 'cron', 'unbound', 'syslog', 'ipsec', 'shaper',
                'monit',
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

    except MODULE_EXCEPTIONS:
        module_dependency_error()

    if target is not None:
        result['changed'] = True
        if not module.check_mode:
            target.reload()

        if hasattr(target, 's'):
            target.s.close()

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
