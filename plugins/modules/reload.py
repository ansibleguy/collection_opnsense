#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to reload running config
# pylint: disable=R0912,R0915,R0914

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/general/reload.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/general/reload.html'


def run_module():
    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['tgt', 't'],
            choices=[
                'alias',
                'rule',
                'route',
                'gateway',
                'cron',
                'unbound',
                'syslog',
                'ipsec',
                'ipsec_legacy',
                'shaper',
                'monit',
                'wireguard',
                'interface_vlan',
                'interface_vxlan',
                'interface_vip',
                'interface_lagg',
                'frr',
                'webproxy',
                'bind',
                'ids',
                'openvpn',
                'dhcrelay',
                'dhcp', 'kea',
                'dnsmasq',
                'haproxy',
                'wazuh',
                'nat_source',
                'nat_one_to_one',
                'nat_destination',
                'nut',
            ],
            description='What part of the running config should be reloaded'
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

    target = module.params['target']
    Target_Obj = None

    try:
        # NOTE: dynamic imports not working as Ansible will not copy those modules to the temporary directory
        #   the module is executed in!
        #   see: ansible.executor.module_common.ModuleDepFinder (analyzing imports to know what dependencies to copy)

        if target == 'alias':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.alias import \
                Alias as Target_Obj

        elif target == 'rule':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.rule import \
                Rule as Target_Obj

        elif target == 'route':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.route import \
                Route as Target_Obj

        elif target == 'gateway':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.gateway import \
                Gw as Target_Obj

        elif target == 'cron':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.cron import \
                CronJob as Target_Obj

        elif target == 'unbound':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.unbound_host import \
                Host as Target_Obj

        elif target == 'syslog':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.syslog import \
                Syslog as Target_Obj

        elif target == 'ipsec':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.ipsec_connection import \
                Connection as Target_Obj

        elif target == 'ipsec_legacy':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.ipsec_cert import \
                KeyPair as Target_Obj

        elif target == 'shaper':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.shaper_pipe import \
                Pipe as Target_Obj
            module.params['reset'] = False

        elif target == 'monit':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.monit_service import \
                Service as Target_Obj

        elif target == 'wireguard':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.wireguard_server import \
                Server as Target_Obj

        elif target == 'interface_vlan':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.interface_vlan import \
                Vlan as Target_Obj

        elif target == 'interface_vxlan':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.interface_vxlan import \
                Vxlan as Target_Obj

        elif target == 'interface_vip':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.interface_vip import \
                Vip as Target_Obj

        elif target == 'interface_lagg':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.interface_lagg import \
                Lagg as Target_Obj

        elif target == 'frr':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.frr_bgp_general import \
                General as Target_Obj

        elif target == 'webproxy':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.webproxy_general import \
                General as Target_Obj

        elif target == 'bind':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.bind_domain import \
                Domain as Target_Obj

        elif target == 'ids':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.ids_general import \
                General as Target_Obj

        elif target == 'openvpn':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.openvpn_client import \
                Client as Target_Obj

        elif target == 'dhcrelay':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dhcrelay_relay import \
                DhcRelayRelay as Target_Obj

        elif target in ['dhcp', 'kea']:
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dhcp_reservation_v4 import \
                ReservationV4 as Target_Obj

        elif target == 'wazuh':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.wazuh_agent import \
                WazuhAgent as Target_Obj

        elif target in ['dnsmasq']:
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dnsmasq_general import \
                General as Target_Obj

        elif target in ['haproxy']:
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_general_settings import \
                HaproxyGeneralSettings as Target_Obj

        elif target == 'nat_source':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_source import \
                SNat as Target_Obj

        elif target == 'nat_one_to_one':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_one_to_one import \
                OneToOne as Target_Obj

        elif target == 'nat_destination':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_destination import \
                DNat as Target_Obj

        elif target == 'nut':
            from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nut import \
                Nut as Target_Obj

    except MODULE_EXCEPTIONS:
        module_dependency_error()

    if Target_Obj is not None:
        target_inst = Target_Obj(module=module, result=result)

        result['changed'] = True
        if not module.check_mode:
            target_inst.reload()

        if hasattr(target_inst, 's'):
            target_inst.s.close()

    else:
        module.fail_json(f"Got unsupported target: '{target}'")

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
