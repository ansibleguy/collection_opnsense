#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_base import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_helper import check_or_load_credentials
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_helper import validate_values, get_alias, equal_type

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/use_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/use_alias.md'


class Alias:
    def __init__(self, module: AnsibleModule, result: dict):
        self.m = module
        self.r = result
        check_or_load_credentials(module=module)
        self.s = Session(module=module)
        self.exists = False
        self.alias = None
        self.uuid = None
        self.check()

    def check(self):
        # pulling alias info if it exists
        existing_aliases = self.s.get(call_config={
            **self.m.params, **{'command': 'searchItem'}
        })
        self.alias = get_alias(aliases=existing_aliases['rows'], name=self.m.params['name'])
        self.exists = len(self.alias) > 0
        if self.exists:
            self.uuid = self.s.get(call_config={
                **self.m.params, **{
                    'command': 'getAliasUUID',
                    'params': [self.m.params['name']],
                }
            })['uuid']

            self.m.params.update({
                'params': [self.uuid],
            })

        if not self.exists and self.m.params['state'] == 'present':
            if self.m.params['content'] is None or len(self.m.params['content']) == 0:
                self.m.fail_json('You need to provide values to create an alias!')

            validate_values(module=self.m)

    def create(self):
        # creating alias
        self.r['changed'] = True
        self.r['diff']['after'] = {self.m.params['name']: self.m.params['content']}
        if not self.m.check_mode:
            self.s.post(call_config={
                **self.m.params, **{
                    'command': 'addItem',
                    'data': {
                        'alias': {
                            'name': self.m.params['name'],
                            'description': self.m.params['description'],
                            'type': self.m.params['type'],
                            'content': '\n'.join(self.m.params['content']),
                            # 'updatefreq': module.params['updatefreq_days'],
                        }
                    },
                }
            })

    def update(self):
        # checking if alias changed
        if equal_type(existing=self.alias['type'], configured=self.m.params['type']):
            _before = self.alias['content'].split(',')
            _after = self.m.params['content']
            _before.sort()
            _after.sort()
            self.r['changed'] = _before != _after
            self.r['diff']['before'] = {self.m.params['name']: _before}
            self.r['diff']['after'] = {self.m.params['name']: _after}

            if self.r['changed'] and not self.m.check_mode:
                # updating alias
                self.s.post(call_config={
                    **self.m.params, **{
                        'command': 'setItem',
                        'data': {
                            'alias': {
                                'name': self.m.params['name'],
                                'description': self.m.params['description'],
                                'type': self.m.params['type'],
                                'content': '\n'.join(self.m.params['content']),
                            }
                        },
                    }
                })

        else:
            self.r['changed'] = True
            self.m.fail_json(
                f"Unable to update alias '{self.m.params['name']}' - it is not of the same type! "
                f"You need to delete the current one first!"
            )

    def delete(self):
        self.r['changed'] = True
        if not self.m.check_mode:
            # NOTE: there is currently no practical way to check if the alias is in use..
            alias_deletion = self.s.post(call_config={
                **self.m.params, **{
                    'command': 'delItem',
                    'allowed_http_stati': [200, 'failed'],  # allowing 'failed' to catch it with a warning
                }
            })

            if 'status' in alias_deletion and alias_deletion['status'] == 'failed':
                self.r['changed'] = False
                self.m.warn(f"Unable to delete alias '{self.m.params['name']}' as it is currently referenced!")

        if self.r['changed']:
            self.r['diff']['before'] = {self.m.params['name']: self.alias['content'].split(',')}

    def enable(self):
        if self.exists and self.alias['enabled'] != '1':
            self.r['changed'] = True
            self.r['diff']['before'] = {self.m.params['name']: {'enabled': False}}
            self.r['diff']['after'] = {self.m.params['name']: {'enabled': True}}

            if not self.m.check_mode:
                self.s.post(call_config={
                    **self.m.params, **{
                        'command': 'toggleItem',
                        'params': [self.uuid, 1],
                    }
                })

    def disable(self):
        if (self.exists and self.alias['enabled'] != '0') or not self.exists:
            self.r['changed'] = True
            self.r['diff']['before'] = {self.m.params['name']: {'enabled': True}}
            self.r['diff']['after'] = {self.m.params['name']: {'enabled': False}}

            if not self.m.check_mode:
                self.s.post(call_config={
                    **self.m.params, **{
                        'command': 'toggleItem',
                        'params': [self.uuid, 0],
                    }
                })


def run_module():
    module_args = dict(
        firewall=dict(type='str', required=True),
        name=dict(type='str', required=True),
        description=dict(type='str', required=False, default=''),
        content=dict(type='list', required=False, default=[]),
        type=dict(type='str', required=False, choices=[
            'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup',
            'mac', 'dynipv6host', 'internal', 'external',
        ], default='host'),
        state=dict(type='str', default='present', required=False, choices=['present', 'absent']),
        enabled=dict(type='bool', required=False, default=True),
        api_key=dict(type='str', required=False),
        api_secret=dict(type='str', required=False, no_log=True),
        api_credential_file=dict(type='str', required=False),
        ssl_verify=dict(type='bool', required=False, default=True),
        debug=dict(type='bool', required=False, default=False),
        # todo: updatefreq not yet working (used by 'urltable')
        # updatefreq_days=dict(type='int', required=False),
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

    # static defaults
    module.params.update({
        'module': 'firewall',
        'controller': 'alias',
        'allowed_http_stati': [200, 'done'],
    })
    # if module.params['updatefreq_days'] is None:
    #     module.params['updatefreq_days'] = ''

    alias = Alias(module=module, result=result)
    if module.params['state'] == 'absent':
        if alias.exists:
            alias.delete()

    else:
        if module.params['content'] is not None and len(module.params['content']) > 0:
            if alias.exists:
                alias.update()

            else:
                alias.create()

        # dis-/enabling
        if alias.exists:
            if module.params['enabled']:
                alias.enable()

            else:
                alias.disable()

    alias.s.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
