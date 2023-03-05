#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to interact with system services

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
        single_get, single_post

except MODULE_EXCEPTIONS:
    module_dependency_error()


DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/service.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/service.html'

# c = api-module, m = custom action-mapping, a = limited actions
SERVICES = {
    # core api
    'captive_portal': {'c': 'captiveportal', 'a': ['reload']},
    'cron': {'a': ['reload']},
    'ipsec_legacy': {'c': 'legacy_subsystem', 'a': ['reload'], 'm': {'reload': 'applyConfig'}},
    'ipsec': {}, 'monit': {}, 'syslog': {},
    'shaper': {'c': 'trafficshaper', 'm': {'restart': 'flushreload', 'status': 'statistics'}},
    #   note: these would support more actions:
    'ids': {}, 'proxy': {}, 'unbound': {},
    # plugins
    'ftp_proxy': {'c': 'ftpproxy'},
    'iperf': {'a': ['reload', 'status', 'start', 'restart']},
    'mdns_repeater': {'c': 'mdnsrepeater', 'a': ['stop', 'status', 'start', 'restart']},
    'munin_node': {'c': 'muninnode'},
    'node_exporter': {'c': 'nodeexporter'},
    'puppet_agent': {'c': 'puppetagent'},
    'qemu_guest_agent': {'c': 'qemuguestagent'},
    'frr': {'c': 'quagga'},
    'radsec_proxy': {'c': 'radsecproxy'},
    'zabbix_agent': {'c': 'zabbixagent'},
    'zabbix_proxy': {'c': 'zabbixproxy'},
    'apcupsd': {}, 'bind': {}, 'chrony': {}, 'cicap': {}, 'collectd': {},
    'dyndns': {}, 'fetchmail': {}, 'freeradius': {}, 'haproxy': {}, 'maltrail': {},
    'netdata': {}, 'netsnmp': {}, 'nrpe': {}, 'nut': {}, 'openconnect': {}, 'proxysso': {},
    'rspamd': {}, 'shadowsocks': {}, 'softether': {}, 'sslh': {}, 'stunnel': {}, 'tayga': {},
    'telegraf': {}, 'tftp': {}, 'tinc': {}, 'wireguard': {},
    #   note: these would support more actions:
    'acme_client': {'c': 'acmeclient'},
    'crowdsec': {'a': ['reload', 'status']},
    'dns_crypt_proxy': {'c': 'dnscryptproxy'},
    'udp_broadcast_relay': {'c': 'udpbroadcastrelay'},
    'clamav': {}, 'hwprobe': {}, 'lldpd': {}, 'nginx': {}, 'ntopng': {}, 'postfix': {}, 'redis': {},
    'relayd': {}, 'siproxd': {}, 'vnstat': {}, 'tor': {},
}

ACTION_MAPPING = {'reload': 'reconfigure'}
API_CONTROLLER = 'service'


def run_module():
    service_choices = list(SERVICES.keys())
    service_choices.sort()

    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['service', 'svc', 'target', 'n'],
            choices=service_choices,
            description='What service to interact with'
        ),
        action=dict(
            type='str', required=True, aliases=['do', 'a'],
            choices=['reload', 'restart', 'start', 'status', 'stop'],
        ),
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    name = module.params['name']
    action = module.params['action']
    service = SERVICES[name]

    if 'a' in service and action not in service['a']:
        module.fail_json(
            f"Service '{name}' does not support the "
            f"provided action '{action}'! "
            f"Supported ones are: {service['a']}"
        )

    # translate actions to api-commands
    # pylint: disable=R1715
    if 'm' in service and action in service['m']:
        action = service['m'][action]

    elif action in ACTION_MAPPING:
        action = ACTION_MAPPING[action]

    result['executed'] = action

    # get api-module
    if 'c' in service:
        api_module = service['c']

    else:
        api_module = name

    # pull status or execute action
    if module.params['action'] == 'status':
        info = single_get(
            module=module,
            cnf={
                'module': api_module,
                'controller': API_CONTROLLER,
                'command': action,
            }
        )

        if 'response' in info:
            info = info['response']

            if isinstance(info, str):
                info = info.strip()

        result['data'] = info

    else:
        result['changed'] = True

        if not module.check_mode:
            single_post(
                module=module,
                cnf={
                    'module': api_module,
                    'controller': API_CONTROLLER,
                    'command': action,
                }
            )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
