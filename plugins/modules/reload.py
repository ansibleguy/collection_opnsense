#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to reload running config

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_dot_obj import DnsOverTls

except MODULE_EXCEPTIONS:
    module_dependency_error()


DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md'


def run_module():
    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['dom', 'd'],
            choises=[
                'alias', 'rule', 'route', 'cron', 'unbound', 'syslog',
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

    if module.params['target'] == 'alias':
        from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
        target = Alias(module=module, result=result)

    elif module.params['target'] == 'rule':
        from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule
        target = Rule(module=module, result=result)

    elif module.params['target'] == 'route':
        from ansible_collections.ansibleguy.opnsense.plugins.module_utils.route_obj import Route
        target = Route(module=module, result=result)

    elif module.params['target'] == 'cron':
        from ansible_collections.ansibleguy.opnsense.plugins.module_utils.cron_obj import CronJob
        target = CronJob(module=module, result=result)

    elif module.params['target'] == 'unbound':
        from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_host_obj import Host
        target = Host(module=module, result=result)

    elif module.params['target'] == 'syslog':
        from ansible_collections.ansibleguy.opnsense.plugins.module_utils.syslog_obj import Syslog
        target = Syslog(module=module, result=result)

    if target is not None:
        result['changed'] = True
        if not module.check_mode:
            target.reconfigure()

        if hasattr(target, 's'):
            target.s.close()

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
