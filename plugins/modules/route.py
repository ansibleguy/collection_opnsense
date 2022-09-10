#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/routes.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.route_obj import Route

except MODULE_EXCEPTIONS:
    module_dependency_error()

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_route.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_route.md'


def run_module():
    module_args = dict(
        gateway=dict(
            type='str', required=True, aliases=['gw'],
            description='Specify a valid existing gateway matching the networks ip protocol'
        ),
        network=dict(
            type='str', required=True, aliases=['nw', 'net'],
            description='Specify a valid network matching the gateways ip protocol'
        ),
        description=dict(type='str', required=False, default='', aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured routes with the running config - '
                        "if any of those fields are changed, the module will think it's a new route",
            choises=['network', 'gateway', 'description'],
            default=['network', 'gateway'],
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

    route = Route(module=module, result=result)
    route.check()
    route.process()
    if result['changed'] and module.params['reload']:
        route.reload()

    route.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
