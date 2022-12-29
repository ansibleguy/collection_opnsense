#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# template to be copied to implement new modules

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_parent import Parent

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'


def run_module():
    module_args = dict(
        host=dict(
            type='str', required=False, default='', aliases=['ip'],
            description='Parent proxy IP address or hostname'
        ),
        auth=dict(
            type='bool', required=False, default=False,
            description='Enable authentication against the parent proxy'
        ),
        user=dict(
            type='str', required=False, default='placeholder',
            description='Set a username if parent proxy requires authentication'
        ),
        password=dict(
            type='str', required=False, default='placeholder', no_log=True,
            description='Set a username if parent proxy requires authentication'
        ),
        port=dict(type='str', required=False, default='', aliases=['p']),
        local_domains=dict(
            type='list', elements='str', required=False, default=[], aliases=['domains'],
            description='Domains not to be sent via parent proxy'
        ),
        local_ips=dict(
            type='list', elements='str', required=False, default=[], aliases=['ips'],
            description='IP addresses not to be sent via parent proxy'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
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

    p = Parent(module=module, result=result)

    def process():
        p.check()
        p.process()
        if result['changed'] and module.params['reload']:
            p.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='webproxy_parent.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    p.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
