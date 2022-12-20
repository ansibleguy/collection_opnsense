#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to reload running config
# pylint: disable=R0912,R0915,R0914

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()


DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/list.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/modules/list.html'


def run_module():
    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['tgt', 't'],
            choises=[
                'alias', 'rule', 'route', 'cron', 'syslog', 'package',
                'unbound_host', 'unbound_domain', 'unbound_dot', 'unbound_forward',
                'unbound_host_alias', 'ipsec_cert', 'shaper_pipe', 'shaper_queue',
                'shaper_rule', 'monit_service', 'monit_test', 'monit_alert',
                'wireguard_server', 'wireguard_peer', 'interface_vlan',
                'interface_vxlan', 'source_nat', 'frr_bfd_neighbor', 'frr_bgp_general',
                'frr_bgp_neighbor', 'frr_bgp_prefix_list', 'frr_bgp_community_list',
                'frr_bgp_as_path', 'frr_ospf_general', 'frr_ospf3_general',
                'frr_ospf3_interface', 'frr_ospf_prefix_list', 'frr_ospf_interface',
                'frr_ospf_route_map', 'frr_ospf_network', 'frr_rip', 'bind_general',
                'bind_blocklist', 'bind_acl', 'bind_domain', 'bind_record',
            ],
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

    target = None

    try:
        # todo: refactor to use config-dict and dynamic imports

        if module.params['target'] == 'alias':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.alias import Alias
            target = Alias(module=module, result=result)

        elif module.params['target'] == 'rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule import Rule
            target = Rule(module=module, result=result)

        elif module.params['target'] == 'route':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.route import Route
            target = Route(module=module, result=result)

        elif module.params['target'] == 'cron':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.cron import CronJob
            target = CronJob(module=module, result=result)

        elif module.params['target'] == 'unbound_host':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_host import Host
            target = Host(module=module, result=result)

        elif module.params['target'] == 'unbound_host_alias':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_host_alias \
                import Alias
            target = Alias(module=module, result=result)

        elif module.params['target'] == 'unbound_domain':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_domain import Domain
            target = Domain(module=module, result=result)

        elif module.params['target'] == 'unbound_dot':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_dot \
                import DnsOverTls
            target = DnsOverTls(module=module, result=result)

        elif module.params['target'] == 'unbound_forward':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_forward \
                import Forward
            target = Forward(module=module, result=result)

        elif module.params['target'] == 'syslog':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.syslog import Syslog
            target = Syslog(module=module, result=result)

        elif module.params['target'] == 'package':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.package import Package
            target = Package(module=module, name='dummy')

        elif module.params['target'] == 'ipsec_cert':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_cert import KeyPair
            target = KeyPair(module=module, result=result)

        elif module.params['target'] == 'shaper_pipe':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_pipe import Pipe
            target = Pipe(module=module, result=result)

        elif module.params['target'] == 'shaper_queue':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_queue import Queue
            target = Queue(module=module, result=result)

        elif module.params['target'] == 'shaper_rule':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_rule import Rule
            target = Rule(module=module, result=result)

        elif module.params['target'] == 'monit_service':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_service import Service
            target = Service(module=module, result=result)

        elif module.params['target'] == 'monit_test':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_test import Test
            target = Test(module=module, result=result)

        elif module.params['target'] == 'monit_alert':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_alert import Alert
            target = Alert(module=module, result=result)

        elif module.params['target'] == 'wireguard_server':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wireguard_server \
                import Server
            target = Server(module=module, result=result)

        elif module.params['target'] == 'wireguard_peer':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wireguard_peer import Peer
            target = Peer(module=module, result=result)

        elif module.params['target'] == 'interface_vlan':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vlan import Vlan
            target = Vlan(module=module, result=result)

        elif module.params['target'] == 'interface_vxlan':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vxlan import Vxlan
            target = Vxlan(module=module, result=result)

        elif module.params['target'] == 'source_nat':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.source_nat import SNat
            target = SNat(module=module, result=result)

        elif module.params['target'] == 'frr_bfd_neighbor':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bfd_neighbor import Neighbor
            target = Neighbor(module=module, result=result)

        elif module.params['target'] == 'frr_bgp_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_general \
                import General
            target = General(module=module, result=result)

        elif module.params['target'] == 'frr_bgp_neighbor':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_neighbor \
                import Neighbor
            target = Neighbor(module=module, result=result)

        elif module.params['target'] == 'frr_bgp_prefix_list':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_prefix_list \
                import Prefix
            target = Prefix(module=module, result=result)

        elif module.params['target'] == 'frr_bgp_route_map':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_route_map \
                import RouteMap
            target = RouteMap(module=module, result=result)

        elif module.params['target'] == 'frr_bgp_community_list':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_community_list \
                import Community
            target = Community(module=module, result=result)

        elif module.params['target'] == 'frr_bgp_as_path':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_as_path \
                import AsPath
            target = AsPath(module=module, result=result)

        elif module.params['target'] == 'frr_ospf_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_general \
                import General
            target = General(module=module, result=result)

        elif module.params['target'] == 'frr_ospf3_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf3_general \
                import General
            target = General(module=module, result=result)

        elif module.params['target'] == 'frr_ospf3_interface':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf3_interface \
                import Interface
            target = Interface(module=module, result=result)

        elif module.params['target'] == 'frr_ospf_prefix_list':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_prefix_list \
                import Prefix
            target = Prefix(module=module, result=result)

        elif module.params['target'] == 'frr_ospf_interface':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_interface \
                import Interface
            target = Interface(module=module, result=result)

        elif module.params['target'] == 'frr_ospf_route_map':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_route_map \
                import RouteMap
            target = RouteMap(module=module, result=result)

        elif module.params['target'] == 'frr_ospf_network':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_network \
                import Network
            target = Network(module=module, result=result)

        elif module.params['target'] == 'frr_rip':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_rip \
                import Rip
            target = Rip(module=module, result=result)

        elif module.params['target'] == 'frr_rip':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_rip \
                import Rip
            target = Rip(module=module, result=result)

        elif module.params['target'] == 'bind_general':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_general \
                import General
            target = General(module=module, result=result)

        elif module.params['target'] == 'bind_blocklist':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_blocklist \
                import Blocklist
            target = Blocklist(module=module, result=result)

        elif module.params['target'] == 'bind_acl':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_acl \
                import Acl
            target = Acl(module=module, result=result)

        elif module.params['target'] == 'bind_domain':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_domain \
                import Domain
            target = Domain(module=module, result=result)

        elif module.params['target'] == 'bind_record':
            from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_record \
                import Record
            target = Record(module=module, result=result)

    except MODULE_EXCEPTIONS:
        module_dependency_error()

    result['data'] = None

    if target is not None:
        if hasattr(target, 'get_existing'):
            # has additional filtering
            target_func = getattr(target, 'get_existing')

        elif hasattr(target, 'search_call'):
            target_func = getattr(target, 'search_call')

        elif hasattr(target, '_search_call'):
            target_func = getattr(target, '_search_call')

        else:
            target_func = getattr(target.b, 'get_existing')

        result['data'] = target_func()

        if hasattr(target, 's'):
            target.s.close()

    else:
        module.fail_json(f"Got unsupported target: '{module.params['target']}'")

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
