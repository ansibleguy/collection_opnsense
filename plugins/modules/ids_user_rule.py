#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/ids.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_user_rule import Rule

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/ids.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/ids.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['name', 'desc'],
            description='Unique rule name',
        ),
        source_ip=dict(
            type='str', required=False, aliases=['source', 'src_ip', 'src'],
            description="Set the source IP or network to match. Leave this field empty for using 'any'",
        ),
        destination_ip=dict(
            type='str', required=False, aliases=['destination', 'dst_ip', 'dst'],
            description="Set the destination IP or network to match. Leave this field empty for using 'any'",
        ),
        ssl_fingerprint=dict(
            type='str', required=False, aliases=['fingerprint', 'ssl_fp'],
            description="The SSL fingerprint, for example: "
                        "'B5:E1:B3:70:5E:7C:FF:EB:92:C4:29:E5:5B:AC:2F:AE:70:17:E9:9E'",
        ),
        action=dict(
            type='str', required=False, aliases=['a'], default='alert',
            choices=['alert', 'drop', 'pass'],
            description='Set action to perform here, only used when in IPS mode',
        ),
        bypass=dict(
            type='bool', required=False, aliases=['bp'], default=False,
            description='Set bypass keyword. Increases traffic throughput. Suricata reads a packet, '
                        'decodes it, checks it in the flow table. If the corresponding flow is local '
                        'bypassed then it simply skips all streaming, detection and output and the packet '
                        'goes directly out in IDS mode and to verdict in IPS mode',
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
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

    module_wrapper(Rule(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
