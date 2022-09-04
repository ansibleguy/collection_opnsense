#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
    OPN_MOD_ARGS, STATE_MOD_ARG
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_host_obj import Host


DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host.md'


def run_module():
    module_args = dict(
        hostname=dict(type='str', required=True, aliases=['host', 'h']),
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        record_type=dict(
            type='str', required=False, aliases=['type', 'rr', 'rt'],
            choises=['A', 'AAAA', 'MX'], default='A',
        ),
        value=dict(type='str', required=True, aliases=['server', 'srv', 'mx']),
        prio=dict(
            type='int', required=False, aliases=['mxprio'], default=10,
            description='Priority that is only used for MX record types'
        ),
        description=dict(type='str', required=False, default='', aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured host-overrides with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choises=[
                'hostname', 'domain', 'record_type', 'value',
                'prio', 'description'
            ],
            default=['hostname', 'domain', 'record_type', 'value', 'prio'],
        ),
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

    host = Host(module=module, result=result)

    host.check()
    host.process()

    host.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
