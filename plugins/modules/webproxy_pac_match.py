#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG, STATE_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_pac_match import Match

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'

MONTH_MAPPING = {
    1: 'JAN',
    2: 'FEB',
    3: 'MAR',
    4: 'APR',
    5: 'MAY',
    6: 'JUN',
    7: 'JUL',
    8: 'AUG',
    9: 'SEP',
    10: 'OCT',
    11: 'NOV',
    12: 'DEC',
}

WEEKDAY_MAPPING = {
    1: 'MON',
    2: 'TUE',
    3: 'WED',
    4: 'THU',
    5: 'FRI',
    6: 'SAT',
    7: 'SUN',
}


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, description='Unique name for the match',
        ),
        description=dict(type='str', required=False, default='', aliases=['desc']),
        negate=dict(
            type='bool', required=False, default=False,
            description='Negate this match. '
                        'For example you can match if a host is not inside a network'
        ),
        type=dict(
            type='str', required=False, default='url_matches',
            choices=[
                'url_matches', 'hostname_matches', 'dns_domain_is', 'destination_in_net',
                'my_ip_in_net', 'plain_hostname', 'is_resolvable', 'dns_domain_levels',
                'weekday_range', 'date_range', 'time_range',
            ],
            description='The type of the match. Depending on the match, you will need '
                        'different arguments',
        ),
        hostname=dict(
            type='str', required=False, default='',
            description='A hostname pattern like *.opnsense.org',
        ),
        url=dict(
            type='str', required=False, default='',
            description='A URL pattern like forum.opnsense.org/index*',
        ),
        network=dict(
            type='str', required=False, default='',
            description='The network address to match in CIDR notation for example '
                        'like 127.0.0.1/8 or ::1/128',
        ),
        domain_level_from=dict(
            type='int', required=False, default=0, aliases=['domain_from'],
            description='The minimum amount of dots in the domain name',
        ),
        domain_level_to=dict(
            type='int', required=False, default=0, aliases=['domain_to'],
            description='The maximum amount of dots in the domain name',
        ),
        hour_from=dict(
            type='int', required=False, default=0, aliases=['time_from'],
            description='Start hour for match-period',
        ),
        hour_to=dict(
            type='int', required=False, default=0, aliases=['time_to'],
            description='End hour for match-period',
        ),
        month_from=dict(
            type='int', required=False, default=1, aliases=['date_from'],
            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            description='Start month for match-period',
        ),
        month_to=dict(
            type='int', required=False, default=1, aliases=['date_to'],
            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            description='End month for match-period',
        ),
        weekday_from=dict(
            type='int', required=False, default=1, aliases=['day_from'],
            choices=[1, 2, 3, 4, 5, 6, 7],
            description='Start weekday for match-period. 1 = monday, 7 = sunday',
        ),
        weekday_to=dict(
            type='int', required=False, default=1, aliases=['day_to'],
            choices=[1, 2, 3, 4, 5, 6, 7],
            description='End weekday for match-period. 1 = monday, 7 = sunday',
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
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

    for day_field in ['weekday_from', 'weekday_to']:
        module.params[day_field] = WEEKDAY_MAPPING[module.params[day_field]]

    for month_field in ['month_from', 'month_to']:
        module.params[month_field] = MONTH_MAPPING[module.params[month_field]]

    module_wrapper(Match(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
