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
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/ids.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/ids.html'


def run_module():
    module_args = dict(
        interfaces=dict(
            type='list', elements='str', required=True, aliases=['ints'],
            description='Select interface(s) to use. When enabling IPS, only use physical interfaces here '
                        '(no vlans etc)'
        ),
        block=dict(
            type='bool', required=False, default=False, aliases=['protection', 'ips'],
            description='Enable protection mode (block traffic). '
                        'Before enabling, please disable all hardware offloading first in advanced network!'
        ),
        promiscuous=dict(
            type='bool', required=False, default=False, aliases=['physical', 'vlan'],
            description='For certain setups (like IPS with vlans), this is required to actually capture data '
                        'on the physical interface'
        ),
        syslog_alerts=dict(
            type='bool', required=False, default=False, aliases=['syslog', 'log'],
            description='Send alerts to system log in fast log format. This will not change the alert '
                        'logging used by the product itself'
        ),
        syslog_output=dict(
            type='bool', required=False, default=False, aliases=['log_stdout'],
            description='Send alerts in eve format to syslog, using log level info. This will not change the alert '
                        'logging used by the product itself. Drop logs will only be send to the internal logger, '
                        'due to restrictions in suricata'
        ),
        log_payload=dict(
            type='bool', required=False, default=False, aliases=['log_packet'],
            description='Send packet payload to the log for further analyses'
        ),
        default_packet_size=dict(
            type='int', required=False, aliases=['packet_size'],
            description='With this option, you can set the size of the packets on your network. It is possible that '
                        'bigger packets have to be processed sometimes. The engine can still process these bigger '
                        'packets, but processing it will lower the performance. Unset = system default'
        ),
        log_retention=dict(
            type='int', required=False, default=4, aliases=['log_count'],
            description='Number of logs to keep'
        ),
        local_networks=dict(
            type='list', elements='str', required=False, aliases=['home_networks'],
            default=['192.168.0.0/16', '10.0.0.0/8', '172.16.0.0/12'],
            description='Networks to interpret as local'
        ),
        log_level=dict(
            type='str', required=False,
            choices=['info', 'perf', 'config', 'debug'],
            description='Increase the verbosity of the Suricata application logging by increasing the log level '
                        'from the default. Unset = system default'
        ),
        pattern_matcher=dict(
            type='str', required=False, aliases=['algorithm', 'matcher', 'algo'],
            choices=['ac', 'ac-bs', 'ac-ks', 'hs'],
            description="Select the multi-pattern matcher algorithm to use. Options: unset = system default, "
                        "'ac' = 'Aho-Corasick', 'ac-bs' = 'Aho-Corasick, reduced memory implementation', "
                        "'ac-ks' = 'Aho-Corasick, Ken Steele variant', 'hs' = 'Hyperscan'"
        ),
        log_rotate=dict(
            type='str', required=False, default='weekly',
            choices=['weekly', 'daily'],
            description='Rotate alert logs at provided interval'
        ),
        profile=dict(
            type='str', required=False, aliases=['detect_profile'],
            choices=['low', 'medium', 'high', 'custom'],
            description="The detection engine builds internal groups of signatures. The engine allow us to specify "
                        "the profile to use for them, to manage memory on an efficient way keeping a good performance. "
                        "Unset = system default"
        ),
        profile_toclient_groups=dict(
            type='str', required=False, aliases=['toclient_groups'],
            description='If Custom is specified. The detection engine tries to split out separate signatures into '
                        'groups so that a packet is only inspected against signatures that can actually match. '
                        'As in large rule set this would result in way too many groups and memory usage similar '
                        'groups are merged together'
        ),
        profile_toserver_groups=dict(
            type='str', required=False, aliases=['toserver_groups'],
            description='If Custom is specified. The detection engine tries to split out separate signatures into '
                        'groups so that a packet is only inspected against signatures that can actually match. '
                        'As in large rule set this would result in way too many groups and memory usage similar '
                        'groups are merged together'
        ),
        schedule=dict(
            type='str', required=False, default='ids rule updates', aliases=['update_cron', 'cron'],
            description='Name/Description of an existing cron-job that should be used to update IDS'
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

    module_wrapper(General(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
