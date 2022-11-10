#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_dot import DnsOverTls

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_dot.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_dot.md'


def run_module():
    module_args = dict(
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        target=dict(
            type='str', required=True, aliases=['tgt', 'server', 'srv'],
            description='Server to forward the dns queries to'
        ),
        port=dict(
            type='int', required=False, default=53, aliases=['p'],
            description='DNS port of the target server'
        ),
        verify=dict(
            type='str', required=False, aliases=['common_name', 'cn', 'hostname'], default='',
            description='Verify if CN in certificate matches this value, if not set - '
                        'certificate verification will not be performed!'
        ),
        type=dict(type='str', required=False, choises=['dot'], default='dot'),
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

    dot = DnsOverTls(module=module, result=result)

    def process():
        dot.check()
        dot.process()
        if result['changed'] and module.params['reload']:
            dot.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='unbound_dot.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    dot.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
