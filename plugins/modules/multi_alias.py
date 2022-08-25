#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/use_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/use_alias.md'


def run_module():
    module_args = dict(
        firewall=dict(type='str', required=True),
        aliases=dict(type='dict', required=True),
        api_key=dict(type='str', required=False),
        api_secret=dict(type='str', required=False, no_log=True),
        api_credential_file=dict(type='str', required=False),
        ssl_verify=dict(type='bool', required=False, default=True),
        debug=dict(type='bool', required=False, default=False),
        # todo: updatefreq not yet working (used by 'urltable')
        # updatefreq_days=dict(type='int', required=False),
    )

    # result = dict(
    #     changed=False,
    #     diff={
    #         'before': {},
    #         'after': {},
    #     }
    # )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # # static defaults
    # module.params.update({
    #     'module': 'firewall',
    #     'controller': 'alias',
    #     'allowed_http_stati': [200, 'done'],
    # })
    # if module.params['updatefreq_days'] is None:
    #     module.params['updatefreq_days'] = ''

    # alias = Alias(module=module, result=result)
    # if module.params['state'] == 'absent':
    #     if alias.exists:
    #         alias.delete()
    #
    # else:
    #     if module.params['content'] is not None and len(module.params['content']) > 0:
    #         if alias.exists:
    #             alias.update()
    #
    #         else:
    #             alias.create()
    #
    #     # dis-/enabling
    #     if alias.exists:
    #         if module.params['enabled']:
    #             alias.enable()
    #
    #         else:
    #             alias.disable()
    # alias.s.close()
    # module.exit_json(**result)
    module.fail_json('Not yet implemented - sorry!')


def main():
    run_module()


if __name__ == '__main__':
    main()
