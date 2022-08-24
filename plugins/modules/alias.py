#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = ''
EXAMPLES = ''
RETURN = ''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_base import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_helper import check_or_load_credentials
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_helper import get_only_values, alias_changed, validate_values


def run_module():
    module_args = dict(
        host=dict(type='str', required=True),
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        values=dict(type='list', required=False),
        type=dict(type='str', required=False, choices=[
            'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup',
            'mac', 'dynipv6host', 'internal', 'external',
        ], default='host'),
        state=dict(default='present', choices=['present', 'absent', 'disabled', 'enabled']),
        api_key=dict(type='str', required=False),
        api_secret=dict(type='str', required=False, no_log=True),
        api_credential_file=dict(type='str', required=False),
        ssl_verify=dict(type='bool', required=False, default=True),
        updatefreq_days=dict(type='int', required=False, default=7),
        # allowed_http_stati=dict(type='list', required=False, default=[200]),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
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

    # validation
    check_or_load_credentials(module=module)
    if module.params['state'] != 'absent':
        if module.params['values'] is None or len(module.params['values']) == 0:
            module.fail_json('You need to provide values to create an alias!')

        validate_values(module=module)

    # static defaults
    module.params.update({
        'module': 'firewall',
        'controller': 'alias',
        'params': [module.params['name']],
        'allowed_http_stati': [200, 'done'],
    })

    # initiating session
    api_session = Session(module=module)

    # pulling alias info if it exists
    existing_alias = api_session.get(call_config={
        **module.params, **{
            'controller': 'alias_util',
            'command': 'list',
            'allowed_http_stati': [200, 404],
        }
    })
    exists = len(existing_alias['rows']) > 0
    if exists:
        existing_alias_uuid = api_session.get(call_config={
            **module.params, **{
                'controller': 'alias',
                'command': 'getAliasUUID',
            }
        })['uuid']
    # test = api_session.get(call_config={
    #     **module.params, **{
    #         'command': 'export',
    #         'controller': 'alias',
    #         'params': [],
    #     }
    # })
    # module.warn(f"{test}")

    if module.params['state'] == 'absent':
        if exists:
            result['changed'] = True
            if not module.check_mode:
                # NOTE: there is currently no practical way to check if the alias is in use..
                alias_deletion = api_session.post(call_config={
                    **module.params, **{
                        'command': 'delItem',
                        'allowed_http_stati': [200, 'failed'],  # allowing 'failed' to catch it with a warning
                        'params': [existing_alias_uuid],
                    }
                })

                if alias_deletion['status'] == 'failed':
                    result['changed'] = False
                    module.warn(f"Unable to delete alias '{module.params['name']}' as it is currently referenced!")

            if result['changed']:
                result['diff']['before'] = {module.params['name']: get_only_values(existing_alias['rows'])}

    else:
        if exists:
            # todo: check if value changed
            # result['changed'] = alias_changed(
            #     configured=module.params['values'],
            #     existing=existing_alias['rows'],
            # )

            if result['changed']:
                # check if type is the same
                # update
                pass

        else:
            # creating alias
            result['changed'] = True
            result['diff']['after'] = {module.params['name']: module.params['values']}
            t = {
                **module.params, **{
                    'command': 'addItem',
                    'data': {
                        'values': module.params['name'],
                        'description': module.params['description'],
                        'type': module.params['type'],
                        'content': '\n'.join(module.params['values']),
                        'updatefreq_days': module.params['updatefreq_days'],
                    },
                }
            }
            module.warn(f"{t}")
            response = api_session.post(call_config=t)
            module.warn(f"{response}")

        # todo: enabled/disabled toggleItem call

    api_session.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
