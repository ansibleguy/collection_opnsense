# Ansible Collection to manage OPNsense Firewalls

----

[![Lint Python](https://github.com/O-X-L/ansible-opnsense/actions/workflows/lint-python.yml/badge.svg)](https://github.com/O-X-L/ansible-opnsense/actions/workflows/lint-python.yml)
[![Lint Ansible](https://github.com/O-X-L/ansible-opnsense/actions/workflows/lint-ansible.yml/badge.svg)](https://github.com/O-X-L/ansible-opnsense/actions/workflows/lint-ansible.yml)
[![Unit Test Status](https://github.com/O-X-L/ansible-opnsense/actions/workflows/unit_test.yml/badge.svg)](https://github.com/O-X-L/ansible-opnsense/actions/workflows/unit_test.yml)
[![Ansible Galaxy](https://badges.oss.oxl.app/galaxy.badge.svg)](https://galaxy.ansible.com/ui/repo/published/oxlorg/opnsense)

**Functional Tests**: - (no resources)

----

## Requirements

The [httpx python module](https://www.python-httpx.org/) is used for API communications!

```bash
python3 -m pip install --upgrade httpx
```

Then - install the collection itself:

```bash
# latest version:
ansible-galaxy collection install git+https://github.com/O-X-L/ansible-opnsense.git

# stable/tested version:
ansible-galaxy collection install git+https://github.com/O-X-L/ansible-opnsense.git,26.1.11
## OR
ansible-galaxy collection install oxlorg.opnsense
```

----

## Usage

See: [Docs](https://ansible-opnsense.oxl.app)

[![Docs Uptime](https://status.oxl.at/api/v1/endpoints/1--oxl_opnsense-ansible-collection-docs/uptimes/7d/badge.svg)](https://status.oxl.at/endpoints/1--oxl_opnsense-ansible-collection-docs)

If you DO NOT want to use Ansible - [this fork](https://github.com/O-X-L/opnsense-api-client) provides you with a raw Python3 interface.

----

## Support the project(s)

Support the Open-Source projects that make these modules possible:

* [Donate to OPNsense](https://opnsense.org/donate/) or [Buy the Business-Edition](https://shop.opnsense.com/product-categorie/software_and_licenses/)
* [Contact the ansible-collection maintainer for support](mailto://contact+opnsense@oxl.at)

----

## Contribute

Feel free to contribute to this project using [pull-requests](https://github.com/O-X-L/ansible-opnsense/pulls), [issues](https://github.com/O-X-L/ansible-opnsense/issues) and [discussions](https://github.com/O-X-L/ansible-opnsense/discussions)!

See also: [Contributing](https://github.com/O-X-L/ansible-opnsense/blob/latest/CONTRIBUTING.md)

<img src="https://contrib.rocks/image?repo=O-X-L/ansible-opnsense&max=7" />

----

## Version Support

We try that the `oxlorg.opnsense` modules always support the latest version of OPNsense.

If an API changed, the current module-implementation might fail for firewalls running an older firmware.

I currently try to create a stable release once or twice a year - as this takes 10-20h of work each time for implementing API-fixes.

As [this project is unfunded](https://github.com/O-X-L/ansible-opnsense/discussions/199) we do not actively check for API-changes - if you find missing functionalities you need/want to have please [report it](https://github.com/O-X-L/ansible-opnsense/issues)! Not all features will be implemented!

----


## Modules

**Development States**:

not implemented => development => [testing](https://github.com/O-X-L/ansible-opnsense/tree/latest/tests) => [unstable (_practical testing_)](https://github.com/O-X-L/ansible-opnsense/discussions/85) => stable

### Implemented


| Function                  | Module                                                         | Usage                                                                                                           | State    |
|:--------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:---------|
| **Base**                  | oxlorg.opnsense.list                                           | [Docs](https://ansible-opnsense.oxl.app/general/list.html)                                                      | stable   |
| **Base**                  | oxlorg.opnsense.reload                                         | [Docs](https://ansible-opnsense.oxl.app/general/reload.html)                                                    | stable   |
| **Raw**                   | oxlorg.opnsense.raw                                            | [Docs](https://ansible-opnsense.oxl.app/general/raw.html)                                                       | unstable |
| **Services**              | oxlorg.opnsense.service                                        | [Docs](https://ansible-opnsense.oxl.app/general/service.html)                                                   | stable   |
| **Alias**                 | oxlorg.opnsense.alias                                          | [Docs](https://ansible-opnsense.oxl.app/modules/alias.html)                                                     | stable   | 
| **Alias**                 | oxlorg.opnsense.alias_multi                                    | [Docs](https://ansible-opnsense.oxl.app/modules/alias_multi.html)                                               | stable   |
| **Alias**                 | oxlorg.opnsense.alias_purge                                    | [Docs](https://ansible-opnsense.oxl.app/modules/alias_multi.html#oxlorg-opnsense-alias-purge)                   | unstable |
| **Rules**                 | oxlorg.opnsense.rule                                           | [Docs](https://ansible-opnsense.oxl.app/modules/rule.html)                                                      | stable   |
| **Rules**                 | oxlorg.opnsense.rule_multi                                     | [Docs](https://ansible-opnsense.oxl.app/modules/rule_multi.html)                                                | stable   |
| **Rules**                 | oxlorg.opnsense.rule_purge                                     | [Docs](https://ansible-opnsense.oxl.app/modules/rule_multi.html#oxlorg-opnsense-rule-purge)                     | unstable |
| **Rule Interface Groups** | oxlorg.opnsense.rule_interface_group                           | [Docs](https://ansible-opnsense.oxl.app/modules/rule_interface_group.html#oxlorg-opnsense-rule-interface-group) | stable   |
| **Savepoints**            | oxlorg.opnsense.savepoint                                      | [Docs](https://ansible-opnsense.oxl.app/modules/savepoint.html)                                                 | stable   |
| **Packages**              | oxlorg.opnsense.package                                        | [Docs](https://ansible-opnsense.oxl.app/modules/package.html)                                                   | stable   |
| **System**                | oxlorg.opnsense.system                                         | [Docs](https://ansible-opnsense.oxl.app/modules/system.html)                                                    | stable   |
| **Cron-Jobs**             | oxlorg.opnsense.cron                                           | [Docs](https://ansible-opnsense.oxl.app/modules/cron.html)                                                      | stable   |
| **Routes**                | oxlorg.opnsense.route                                          | [Docs](https://ansible-opnsense.oxl.app/modules/routing.html)                                                   | stable   |
| **Gateways**              | oxlorg.opnsense.gateway                                        | [Docs](https://ansible-opnsense.oxl.app/modules/routing.html)                                                   | stable   |
| **DNS**                   | oxlorg.opnsense.unbound_general                                | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_general.html)                                           | stable   |
| **DNS**                   | oxlorg.opnsense.unbound_acl                                    | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_acl.html)                                               | stable   |
| **DNS**                   | oxlorg.opnsense.unbound_forward                                | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_forwarding.html)                                        | stable   |
| **DNS**                   | oxlorg.opnsense.unbound_dot                                    | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_dot.html)                                               | stable   |
| **DNS**                   | oxlorg.opnsense.unbound_host                                   | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_host.html)                                              | stable   |
| **DNS**                   | oxlorg.opnsense.unbound_host_alias                             | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_host_alias.html)                                        | stable   |
| **DNS**                   | oxlorg.opnsense.unbound_dnsbl                                  | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_host_alias.html)                                        | stable   |
| **Syslog**                | oxlorg.opnsense.syslog                                         | [Docs](https://ansible-opnsense.oxl.app/modules/syslog.html)                                                    | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_connection, oxlorg.opnsense.ipsec_tunnel | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_pool, oxlorg.opnsense.ipsec_network      | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_auth_local                               | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_auth_remote                              | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_child                                    | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_vti                                      | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_cert                                     | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_psk                                      | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.ipsec_manual_spd                               | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | stable   |
| **IPSec**                 | oxlorg.opnsense.general                                        | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                     | unstable |
| **Traffic Shaper**        | oxlorg.opnsense.shaper_pipe                                    | [Docs](https://ansible-opnsense.oxl.app/modules/shaper.html)                                                    | stable   |
| **Traffic Shaper**        | oxlorg.opnsense.shaper_queue                                   | [Docs](https://ansible-opnsense.oxl.app/modules/shaper.html)                                                    | stable   |
| **Traffic Shaper**        | oxlorg.opnsense.shaper_rule                                    | [Docs](https://ansible-opnsense.oxl.app/modules/shaper.html)                                                    | stable   |
| **Monit**                 | oxlorg.opnsense.monit_service                                  | [Docs](https://ansible-opnsense.oxl.app/modules/monit.html)                                                     | stable   |
| **Monit**                 | oxlorg.opnsense.monit_alert                                    | [Docs](https://ansible-opnsense.oxl.app/modules/monit.html)                                                     | stable   |
| **Monit**                 | oxlorg.opnsense.monit_test                                     | [Docs](https://ansible-opnsense.oxl.app/modules/monit.html)                                                     | stable   |
| **WireGuard**             | oxlorg.opnsense.wireguard_server                               | [Docs](https://ansible-opnsense.oxl.app/modules/wireguard.html)                                                 | stable   |
| **WireGuard**             | oxlorg.opnsense.wireguard_peer                                 | [Docs](https://ansible-opnsense.oxl.app/modules/wireguard.html)                                                 | stable   |
| **WireGuard**             | oxlorg.opnsense.wireguard_show                                 | [Docs](https://ansible-opnsense.oxl.app/modules/wireguard.html)                                                 | stable   |
| **WireGuard**             | oxlorg.opnsense.wireguard_general                              | [Docs](https://ansible-opnsense.oxl.app/modules/wireguard.html)                                                 | stable   |
| **Interfaces**            | oxlorg.opnsense.interface_vlan                                 | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                 | stable   |
| **Interfaces**            | oxlorg.opnsense.interface_vxlan                                | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                 | stable   |
| **Interfaces**            | oxlorg.opnsense.interface_vip                                  | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                 | stable   |
| **Interfaces**            | oxlorg.opnsense.interface_lagg                                 | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                 | stable   |
| **Interfaces**            | oxlorg.opnsense.interface_loopback                             | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                 | stable   |
| **Interfaces**            | oxlorg.opnsense.interface_gre                                  | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                 | stable   |
| **Interfaces**            | oxlorg.opnsense.interface_bridge                               | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                 | unstable |
| **Interfaces**            | oxlorg.opnsense.interface_gif                                  | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                 | unstable |
| **NAT**                   | oxlorg.opnsense.nat_source                                     | [Docs](https://ansible-opnsense.oxl.app/modules/nat_source.html)                                                | stable   |
| **NAT**                   | oxlorg.opnsense.nat_destination                                | [Docs](https://ansible-opnsense.oxl.app/modules/nat_destination.html)                                           | unstable |
| **NAT**                   | oxlorg.opnsense.nat_one_to_one                                 | [Docs](https://ansible-opnsense.oxl.app/modules/nat_one_to_one.html)                                            | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_diagnostic                                 | [Docs](https://ansible-opnsense.oxl.app/modules/frr_diagnostic.html)                                            | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_general                                    | [Docs](https://ansible-opnsense.oxl.app/modules/frr_general.html)                                               | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bfd_general                                | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bfd.html#oxlorg-opnsense-frr-bfd-general)                   | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bfd_neighbor                               | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bfd.html#oxlorg-opnsense-frr-bfd-neighbor)                  | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bgp_general                                | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#oxlorg-opnsense-frr-bgp-general)                   | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bgp_neighbor                               | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#oxlorg-opnsense-frr-bgp-neighbor)                  | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bgp_prefix_list                            | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#oxlorg-opnsense-frr-bgp-prefix-list)               | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bgp_route_map                              | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#oxlorg-opnsense-frr-bgp-route-map)                 | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bgp_community_list                         | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#oxlorg-opnsense-frr-bgp-community-list)            | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bgp_as_path                                | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#oxlorg-opnsense-frr-bgp-as-path)                   | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bgp_redistribution                         | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#oxlorg-opnsense-frr-bgp-redistribution)            | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_bgp_peer_group                             | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#oxlorg-opnsense-frr-bgp-peer-group)                | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf_general                               | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf-general)                 | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf_prefix_list                           | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf-prefix-list)             | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf_route_map                             | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf-route-map)               | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf_interface                             | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf-interface)               | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf_network                               | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf-network)                 | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf_redistribution                        | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf-redistribution)          | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf3_general                              | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf3-general)                | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf3_prefix_list                          | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf3-prefix-list)            | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf3_route_map                            | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf3-route-map)              | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf3_interface                            | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf3-interface)              | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf3_network                              | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf3-network)                | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_ospf3_redistribution                       | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#oxlorg-opnsense-frr-ospf3-redistribution)         | stable   |
| **Dynamic Routing**       | oxlorg.opnsense.frr_rip                                        | [Docs](https://ansible-opnsense.oxl.app/modules/frr_rip.html)                                                   | stable   |
| **DNS**                   | oxlorg.opnsense.bind_general                                   | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#oxlorg-opnsense-bind-general)                         | stable   |
| **DNS**                   | oxlorg.opnsense.bind_blocklist                                 | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#oxlorg-opnsense-bind-blocklist)                       | stable   |
| **DNS**                   | oxlorg.opnsense.bind_acl                                       | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#oxlorg-opnsense-bind-acl)                             | stable   |
| **DNS**                   | oxlorg.opnsense.bind_domain                                    | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#oxlorg-opnsense-bind-domain)                          | stable   |
| **DNS**                   | oxlorg.opnsense.bind_record                                    | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#oxlorg-opnsense-bind-record)                          | stable   |
| **DNS**                   | oxlorg.opnsense.bind_record_multi                              | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#oxlorg-opnsense-bind-record-multi)                    | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_general                               | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id2)                                              | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_cache                                 | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id3)                                              | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_parent                                | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id4)                                              | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_traffic                               | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id5)                                              | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_forward                               | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id7)                                              | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_acl                                   | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id8)                                              | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_icap                                  | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id9)                                              | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_auth                                  | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id10)                                             | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_remote_acl                            | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id12)                                             | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_pac_proxy                             | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id14)                                             | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_pac_match                             | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id15)                                             | stable   |
| **Web Proxy**             | oxlorg.opnsense.webproxy_pac_rule                              | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id18)                                             | stable   |
| **IDS/IPS**               | oxlorg.opnsense.ids_action                                     | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id2)                                                   | stable   |
| **IDS/IPS**               | oxlorg.opnsense.ids_general                                    | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id3)                                                   | stable   |
| **IDS/IPS**               | oxlorg.opnsense.ids_ruleset                                    | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id4)                                                   | stable   |
| **IDS/IPS**               | oxlorg.opnsense.ids_rule                                       | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id5)                                                   | stable   |
| **IDS/IPS**               | oxlorg.opnsense.ids_user_rule                                  | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id6)                                                   | stable   |
| **IDS/IPS**               | oxlorg.opnsense.ids_policy                                     | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id7)                                                   | stable   |
| **IDS/IPS**               | oxlorg.opnsense.ids_policy_rule                                | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id8)                                                   | stable   |
| **OpenVPN**               | oxlorg.opnsense.openvpn_client                                 | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                   | stable   |
| **OpenVPN**               | oxlorg.opnsense.openvpn_server                                 | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                   | stable   |
| **OpenVPN**               | oxlorg.opnsense.openvpn_static_key                             | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                   | stable   |
| **OpenVPN**               | oxlorg.opnsense.openvpn_status                                 | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                   | stable   |
| **OpenVPN**               | oxlorg.opnsense.openvpn_client_override                        | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                   | stable   |
| **Nginx**                 | oxlorg.opnsense.nginx_general                                  | [Docs](https://ansible-opnsense.oxl.app/modules/nginx.html#oxlorg-opnsense-nginx-general)                       | stable   |
| **Nginx**                 | oxlorg.opnsense.nginx_upstream_server                          | [Docs](https://ansible-opnsense.oxl.app/modules/nginx.html#oxlorg-opnsense-nginx-upstream-server)               | stable   |
| **DHCP Relay**            | oxlorg.opnsense.dhcrelay_relay                                 | [Docs](https://ansible-opnsense.oxl.app/modules/dhcrelay_relay.html)                                            | stable   |
| **DHCP Relay**            | oxlorg.opnsense.dhcrelay_destination                           | [Docs](https://ansible-opnsense.oxl.app/modules/dhcrelay_destination.html)                                      | stable   |
| **DHCP**                  | oxlorg.opnsense.dhcp_general                                   | [Docs](https://ansible-opnsense.oxl.app/modules/dhcp.html)                                                      | stable   |
| **DHCP Subnet**           | oxlorg.opnsense.dhcp_subnet                                    | [Docs](https://ansible-opnsense.oxl.app/modules/dhcp.html)                                                      | stable   |
| **DHCP Reservation**      | oxlorg.opnsense.dhcp_reservation                               | [Docs](https://ansible-opnsense.oxl.app/modules/dhcp.html)                                                      | stable   |
| **DHCP Controlagent**     | oxlorg.opnsense.dhcp_controlagent                              | [Docs](https://ansible-opnsense.oxl.app/modules/dhcp.html)                                                      | stable   |
| **ACME (Certificates)**   | oxlorg.opnsense.acme_account                                   | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                | stable   |
| **ACME (Certificates)**   | oxlorg.opnsense.acme_action                                    | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                | stable   |
| **ACME (Certificates)**   | oxlorg.opnsense.acme_general                                   | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                | stable   |
| **ACME (Certificates)**   | oxlorg.opnsense.acme_validation                                | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                | stable   |
| **ACME (Certificates)**   | oxlorg.opnsense.acme_certificate                               | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_general                                | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_domain                                 | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_recipient                              | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_recipientbcc                           | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_sender                                 | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_senderbcc                              | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_sendercanonical                        | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_headercheck                            | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Postfix**               | oxlorg.opnsense.postfix_address                                | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                   | stable   |
| **Snapshot**              | oxlorg.opnsense.snapshot                                       | [Docs](https://ansible-opnsense.oxl.app/modules/snapshot.html)                                                  | stable   |
| **High Availability**     | oxlorg.opnsense.hasync_general                                 | [Docs](https://ansible-opnsense.oxl.app/modules/hasync.html)                                                    | stable   |
| **High Availability**     | oxlorg.opnsense.hasync_service                                 | [Docs](https://ansible-opnsense.oxl.app/modules/hasync.html)                                                    | stable   |
| **User Management**       | oxlorg.opnsense.user                                           | [Docs](https://ansible-opnsense.oxl.app/modules/access.html)                                                    | unstable |
| **User Management**       | oxlorg.opnsense.group                                          | [Docs](https://ansible-opnsense.oxl.app/modules/access.html)                                                    | unstable |
| **User Management**       | oxlorg.opnsense.privilege                                      | [Docs](https://ansible-opnsense.oxl.app/modules/access.html)                                                    | unstable |
| **Neighbor**              | oxlorg.opnsense.neighbor                                       | [Docs](https://ansible-opnsense.oxl.app/modules/neighbor.html)                                                  | unstable |
| **Dnsmasq**               | oxlorg.opnsense.dnsmasq_general                                | [Docs](https://ansible-opnsense.oxl.app/modules/dnsmasq.html)                                                   | unstable |
| **Dnsmasq**               | oxlorg.opnsense.dnsmasq_domain                                 | [Docs](https://ansible-opnsense.oxl.app/modules/dnsmasq.html)                                                   | unstable |
| **Dnsmasq**               | oxlorg.opnsense.dnsmasq_host                                   | [Docs](https://ansible-opnsense.oxl.app/modules/dnsmasq.html)                                                   | unstable |
| **Dnsmasq**               | oxlorg.opnsense.dnsmasq_range                                  | [Docs](https://ansible-opnsense.oxl.app/modules/dnsmasq.html)                                                   | unstable |
| **Dnsmasq**               | oxlorg.opnsense.dnsmasq_option                                 | [Docs](https://ansible-opnsense.oxl.app/modules/dnsmasq.html)                                                   | unstable |
| **Dnsmasq**               | oxlorg.opnsense.dnsmasq_boot                                   | [Docs](https://ansible-opnsense.oxl.app/modules/dnsmasq.html)                                                   | unstable |
| **Dnsmasq**               | oxlorg.opnsense.dnsmasq_tag                                    | [Docs](https://ansible-opnsense.oxl.app/modules/dnsmasq.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_general_cache                          | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_general_defaults                       | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_general_logging                        | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_general_peers                          | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_general_settings                       | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_general_stats                          | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_general_tuning                         | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_cpu                                    | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_user                                   | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_group                                  | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_maintenance                            | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_acl                                    | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_lua                                    | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_action                                 | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_errorfile                              | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |
| **HAProxy**               | oxlorg.opnsense.haproxy_fcgi                                   | [Docs](https://ansible-opnsense.oxl.app/modules/haproxy.html)                                                   | unstable |

### Roadmap

New features can currently only be supplied as [Pull Requests](https://github.com/O-X-L/ansible-opnsense/pulls) which have to follow the [Contribution Guidelines](https://github.com/O-X-L/ansible-opnsense/blob/latest/CONTRIBUTING.md) & [Developer Docs](https://ansible-opnsense.oxl.app/usage/4_develop.html).

As there are very few maintainer-resources available for this project, it might take a long time for responses.
