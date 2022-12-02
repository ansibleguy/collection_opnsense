#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/bind.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty, sort_param_lists
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_record import \
        Record

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md'


def run_module():
    module_args = dict(
        domain=dict(type='str', required=True, aliases=['domain_name']),
        name=dict(type='str', required=True, aliases=['record']),
        type=dict(
            type='str', required=False, default='A',
            choises=[
                'A', 'AAAA', 'CAA', 'CNAME', 'DNSKEY', 'DS', 'MX', 'NS', 'PTR',
                'RRSIG', 'SRV', 'TLSA', 'TXT',
            ]
        ),
        value=dict(type='str', required=False, default=''),
        round_robin=dict(
            type='bool', required=False, default=False,
            description='If multiple records with the same domain/name/type combination exist - '
                        "the module will only execute 'state=absent' if set to 'false'. "
                        "To create multiple ones set this to 'true'. "
                        "Records will only be created, NOT UPDATED! (no matching is done)"
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured records with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choises=['domain', 'name', 'type', 'value'],
            default=['domain', 'name', 'type'],
        ),
        **STATE_MOD_ARG,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG,
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

    r = Record(module=module, result=result)

    def process():
        r.check()
        r.process()
        if result['changed'] and module.params['reload']:
            r.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='bind_record.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    r.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
