#!/usr/bin/env python3

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to query running config
# pylint: disable=R0912,R0915,R0914

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/list.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/list.html'

TARGETS = [
    'alias', 'rule', 'route', 'syslog', 'package', 'unbound_host', 'unbound_domain', 'frr_ospf_general',
    'frr_ospf3_general', 'unbound_forward', 'shaper_pipe', 'shaper_queue', 'shaper_rule', 'monit_service',
    'monit_test', 'monit_alert', 'wireguard_server', 'bind_domain', 'wireguard_peer', 'interface_vlan',
    'unbound_host_alias', 'interface_vxlan', 'frr_bfd_neighbor', 'frr_bgp_general', 'frr_bgp_neighbor',
    'frr_ospf3_interface', 'frr_ospf_interface', 'bind_acl', 'frr_ospf_network', 'frr_rip', 'bind_general',
    'bind_blocklist', 'bind_record', 'interface_vip', 'webproxy_general', 'webproxy_cache', 'webproxy_parent',
    'webproxy_traffic', 'webproxy_remote_acl', 'webproxy_pac_proxy', 'webproxy_pac_match', 'webproxy_pac_rule',
    'cron', 'unbound_dot', 'ipsec_cert', 'ipsec_psk', 'source_nat', 'frr_bgp_prefix_list', 'frr_bgp_community_list',
    'frr_bgp_as_path', 'frr_bgp_route_map', 'frr_ospf_prefix_list', 'frr_ospf_route_map', 'webproxy_forward',
    'webproxy_acl', 'webproxy_icap', 'webproxy_auth', 'nginx_upstream_server', 'ipsec_connection', 'ipsec_pool',
    'ipsec_child', 'ipsec_vti', 'ipsec_auth_local', 'ipsec_auth_remote', 'frr_general', 'unbound_general',
    'unbound_acl', 'ids_general', 'ids_policy', 'ids_rule', 'ids_ruleset', 'ids_user_rule', 'ids_policy_rule',
    'openvpn_instance', 'openvpn_static_key', 'openvpn_client_override',
]


def run_module():
    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['tgt', 't'],
            choices=TARGETS,
            description='What part of the running config should be listed'
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
    Target_Obj, target_inst = None, None

    try:
        # NOTE: dynamic imports not working as Ansible will not copy those modules to the temporary directory
        #   the module is executed in!
        #   see: ansible.executor.module_common.ModuleDepFinder (analyzing imports to know what dependencies to copy)

        if target == 'alias':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.alias import \
                Alias as Target_Obj

        elif target == 'rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule import \
                Rule as Target_Obj

        elif target == 'route':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.route import \
                Route as Target_Obj

        elif target == 'cron':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.cron import \
                CronJob as Target_Obj

        elif target == 'unbound_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_general import \
                General as Target_Obj

        elif target == 'unbound_acl':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_acl import \
                Acl as Target_Obj

        elif target == 'unbound_host':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_host import \
                Host as Target_Obj

        elif target == 'unbound_host_alias':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_host_alias \
                import Alias as Target_Obj

        elif target == 'unbound_domain':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_domain import  \
                Domain as Target_Obj

        elif target == 'unbound_dot':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_dot \
                import DnsOverTls as Target_Obj

        elif target == 'unbound_forward':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_forward \
                import Forward as Target_Obj

        elif target == 'syslog':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.syslog import \
                Syslog as Target_Obj

        elif target == 'package':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.package import Package
            target_inst = Package(module=module, name='dummy')

        elif target == 'ipsec_cert':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_cert import \
                KeyPair as Target_Obj

        elif target == 'ipsec_psk':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_psk import \
                PreSharedKey as Target_Obj

        elif target == 'shaper_pipe':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_pipe import \
                Pipe as Target_Obj

        elif target == 'shaper_queue':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_queue import \
                Queue as Target_Obj

        elif target == 'shaper_rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_rule import \
                Rule as Target_Obj

        elif target == 'monit_service':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_service import \
                Service as Target_Obj

        elif target == 'monit_test':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_test import \
                Test as Target_Obj

        elif target == 'monit_alert':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_alert import \
                Alert as Target_Obj

        elif target == 'wireguard_server':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wireguard_server \
                import Server as Target_Obj

        elif target == 'wireguard_peer':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wireguard_peer import \
                Peer as Target_Obj

        elif target == 'interface_vlan':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vlan import \
                Vlan as Target_Obj

        elif target == 'interface_vxlan':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vxlan import \
                Vxlan as Target_Obj

        elif target == 'source_nat':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.source_nat import \
                SNat as Target_Obj

        elif target == 'frr_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_general \
                import General as Target_Obj

        elif target == 'frr_bfd_neighbor':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bfd_neighbor import \
                Neighbor as Target_Obj

        elif target == 'frr_bgp_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_general \
                import General as Target_Obj

        elif target == 'frr_bgp_neighbor':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_neighbor \
                import Neighbor as Target_Obj

        elif target == 'frr_bgp_prefix_list':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_prefix_list \
                import Prefix as Target_Obj

        elif target == 'frr_bgp_route_map':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_route_map \
                import RouteMap as Target_Obj

        elif target == 'frr_bgp_community_list':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_community_list \
                import Community as Target_Obj

        elif target == 'frr_bgp_as_path':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_as_path \
                import AsPath as Target_Obj

        elif target == 'frr_ospf_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_general \
                import General as Target_Obj

        elif target == 'frr_ospf3_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf3_general \
                import General as Target_Obj

        elif target == 'frr_ospf3_interface':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf3_interface \
                import Interface as Target_Obj

        elif target == 'frr_ospf_prefix_list':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_prefix_list \
                import Prefix as Target_Obj

        elif target == 'frr_ospf_interface':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_interface \
                import Interface as Target_Obj

        elif target == 'frr_ospf_route_map':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_route_map \
                import RouteMap as Target_Obj

        elif target == 'frr_ospf_network':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_network \
                import Network as Target_Obj

        elif target == 'frr_rip':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_rip \
                import Rip as Target_Obj

        elif target == 'bind_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_general \
                import General as Target_Obj

        elif target == 'bind_blocklist':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_blocklist \
                import Blocklist as Target_Obj

        elif target == 'bind_acl':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_acl \
                import Acl as Target_Obj

        elif target == 'bind_domain':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_domain \
                import Domain as Target_Obj

        elif target == 'bind_record':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_record \
                import Record as Target_Obj

        elif target == 'interface_vip':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vip import \
                Vip as Target_Obj

        elif target == 'webproxy_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_general import \
                General as Target_Obj

        elif target == 'webproxy_cache':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_cache import \
                Cache as Target_Obj

        elif target == 'webproxy_traffic':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_traffic import \
                Traffic as Target_Obj

        elif target == 'webproxy_parent':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_parent import \
                Parent as Target_Obj

        elif target == 'webproxy_forward':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_forward import \
                General as Target_Obj

        elif target == 'webproxy_acl':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_acl import \
                General as Target_Obj

        elif target == 'webproxy_icap':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_icap import \
                General as Target_Obj

        elif target == 'webproxy_auth':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_auth import \
                General as Target_Obj

        elif target == 'webproxy_remote_acl':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_remote_acl import \
                Acl as Target_Obj

        elif target == 'webproxy_pac_proxy':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_pac_proxy import \
                Proxy as Target_Obj

        elif target == 'webproxy_pac_match':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_pac_match import \
                Match as Target_Obj

        elif target == 'webproxy_pac_rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_pac_rule import \
                Rule as Target_Obj

        elif target == 'nginx_upstream_server':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.nginx_upstream_server import \
                UpstreamServer as Target_Obj

        elif target == 'ipsec_connection':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_connection import \
                Connection as Target_Obj

        elif target == 'ipsec_pool':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_pool import \
                Pool as Target_Obj

        elif target == 'ipsec_child':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_child import \
                Child as Target_Obj

        elif target == 'ipsec_vti':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_vti import \
                Vti as Target_Obj

        elif target == 'ipsec_auth_local':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_auth_local import \
                Auth as Target_Obj

        elif target == 'ipsec_auth_remote':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_auth_remote import \
                Auth as Target_Obj

        elif target == 'ids_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_general import \
                General as Target_Obj

        elif target == 'ids_policy':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_policy import \
                Policy as Target_Obj

        elif target == 'ids_rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_rule import \
                Rule as Target_Obj

        elif target == 'ids_ruleset':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_ruleset import \
                Ruleset as Target_Obj

        elif target == 'ids_user_rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_user_rule import \
                Rule as Target_Obj

        elif target == 'ids_policy_rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_policy_rule import \
                Rule as Target_Obj

        elif target == 'openvpn_instance':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.openvpn_client import \
                Client as Target_Obj

        elif target == 'openvpn_static_key':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.openvpn_static_key import \
                Key as Target_Obj

        elif target == 'openvpn_client_override':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.openvpn_client_override import \
                Override as Target_Obj

    except AttributeError:
        module_dependency_error()

    result['data'] = None

    if Target_Obj is not None or target_inst is not None:
        if target_inst is None:
            target_inst = Target_Obj(module=module, result=result)

        if hasattr(target_inst, 'get_existing'):
            # has additional filtering
            target_func = getattr(target_inst, 'get_existing')

        elif hasattr(target_inst, 'search_call'):
            target_func = getattr(target_inst, 'search_call')

        elif hasattr(target_inst, '_search_call'):
            target_func = getattr(target_inst, '_search_call')

        else:
            target_func = getattr(target_inst.b, 'get_existing')

        result['data'] = target_func()

        if hasattr(target_inst, 's'):
            target_inst.s.close()

    else:
        module.fail_json(f"Got unsupported target: '{target}'")

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
