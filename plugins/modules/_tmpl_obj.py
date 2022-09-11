#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# template to be copied to implement new modules

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
        OPN_MOD_ARGS, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils._tmpl_obj import TMPL

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/_tmpl.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/_tmpl.md'


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str', required=False, default='', aliases=['desc']),
        content=dict(type='list', required=False, default=[], elements='str'),
        type=dict(type='str', required=False, choices=['1', '2'], default='1'),
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

    tmpl = TMPL(module=module, result=result)

    def process():
        tmpl.check()
        tmpl.process()
        if result['changed'] and module.params['reload']:
            tmpl.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='tmpl.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    tmpl.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
