# Ansible Collection - ansibleguy.opnsense

[![Functional Test Status](https://badges.ansibleguy.net/opnsense.collection.test.svg)](https://github.com/ansibleguy/collection_opnsense/blob/stable/scripts/test.sh)
[![Lint Test Status](https://badges.ansibleguy.net/opnsense.collection.lint.svg)](https://github.com/ansibleguy/collection_opnsense/blob/stable/scripts/lint.sh)
[![Docs](https://readthedocs.org/projects/opnsense_ansible/badge/?version=latest&style=flat)](https://opnsense.ansibleguy.net)

----

## Contribute

Feel free to contribute to this project using [pull-requests](https://github.com/ansibleguy/collection_opnsense/pulls), [issues](https://github.com/ansibleguy/collection_opnsense/issues) and [discussions](https://github.com/ansibleguy/collection_opnsense/discussions)!

**What to contribute**:

* add ansible-based [tests](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests) for some error-case(s) you have encountered
* extend or correct the [documentation](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs)
* contribute code fixes or optimizations
* implement additional API endpoints => see [development guide](https://opnsense.ansibleguy.net/usage/4_develop.html)
* test unstable modules and report bugs/errors

----

## Requirements

The [httpx python module](https://www.python-httpx.org/) is used for API communications!

```bash
python3 -m pip install httpx
```

Then - install the collection itself:

```bash
# stable/tested version:
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git,1.1.0

# latest version:
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git

# install to specific director for easier development
cd $PLAYBOOK_DIR
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git -p ./collections
```

----

## Usage

See: [Docs](https://opnsense.ansibleguy.net)

----

## Modules

**Development States**:

not implemented => development => [testing](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests) => unstable (_practical testing_) => stable

### Implemented


| Function            | Module                                     | Usage                                                                                                   | State                 |
|:--------------------|:-------------------------------------------|:--------------------------------------------------------------------------------------------------------|:----------------------|
| **Base**            | ansibleguy.opnsense.list                   | [Docs](https://opnsense.ansibleguy.net/modules/2_list.html)                                             | stable                |
| **Base**            | ansibleguy.opnsense.reload                 | [Docs](https://opnsense.ansibleguy.net/modules/2_reload.html)                                           | stable                |
| **Services**        | ansibleguy.opnsense.service                | [Docs](https://opnsense.ansibleguy.net/modules/service.html)                                            | stable                |
| **Alias**           | ansibleguy.opnsense.alias                  | [Docs](https://opnsense.ansibleguy.net/modules/alias.html)                                              | stable                | 
| **Alias**           | ansibleguy.opnsense.alias_multi            | [Docs](https://opnsense.ansibleguy.net/modules/alias_multi.html)                                        | stable                |
| **Alias**           | ansibleguy.opnsense.alias_purge            | [Docs](https://opnsense.ansibleguy.net/modules/alias_multi.html#ansibleguy-opnsense-alias-purge)        | unstable              |
| **Rules**           | ansibleguy.opnsense.rule                   | [Docs](https://opnsense.ansibleguy.net/modules/rule.html)                                               | unstable              |
| **Rules**           | ansibleguy.opnsense.rule_multi             | [Docs](https://opnsense.ansibleguy.net/modules/rule_multi.html)                                         | unstable              |
| **Rules**           | ansibleguy.opnsense.rule_purge             | [Docs](https://opnsense.ansibleguy.net/modules/rule_multi.html#ansibleguy-opnsense-rule-purge)          | unstable              |
| **Savepoints**      | ansibleguy.opnsense.savepoint              | [Docs](https://opnsense.ansibleguy.net/modules/savepoint.html)                                          | unstable              |
| **Packages**        | ansibleguy.opnsense.package                | [Docs](https://opnsense.ansibleguy.net/modules/package.html)                                            | stable                |
| **System**          | ansibleguy.opnsense.system                 | [Docs](https://opnsense.ansibleguy.net/modules/system.html)                                             | unstable              |
| **Cron-Jobs**       | ansibleguy.opnsense.cron                   | [Docs](https://opnsense.ansibleguy.net/modules/cron.html)                                               | unstable              |
| **Routes**          | ansibleguy.opnsense.route                  | [Docs](https://opnsense.ansibleguy.net/modules/route.html)                                              | unstable              |
| **DNS**             | ansibleguy.opnsense.unbound_forward        | [Docs](https://opnsense.ansibleguy.net/modules/unbound_forwarding.html)                                 | stable                |
| **DNS**             | ansibleguy.opnsense.unbound_dot            | [Docs](https://opnsense.ansibleguy.net/modules/unbound_dot.html)                                        | stable                |
| **DNS**             | ansibleguy.opnsense.unbound_host           | [Docs](https://opnsense.ansibleguy.net/modules/unbound_host.html)                                       | stable                |
| **DNS**             | ansibleguy.opnsense.unbound_domain         | [Docs](https://opnsense.ansibleguy.net/modules/unbound_domain.html)                                     | stable                |
| **DNS**             | ansibleguy.opnsense.unbound_host_alias     | [Docs](https://opnsense.ansibleguy.net/modules/unbound_host_alias.html)                                 | unstable              |
| **Syslog**          | ansibleguy.opnsense.syslog                 | [Docs](https://opnsense.ansibleguy.net/modules/syslog.html)                                             | stable                |
| **IPSec**           | ansibleguy.opnsense.ipsec_cert             | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                              | unstable              |
| **Traffic Shaper**  | ansibleguy.opnsense.shaper_pipe            | [Docs](https://opnsense.ansibleguy.net/modules/shaper.html)                                             | unstable              |
| **Traffic Shaper**  | ansibleguy.opnsense.shaper_queue           | [Docs](https://opnsense.ansibleguy.net/modules/shaper.html)                                             | unstable              |
| **Traffic Shaper**  | ansibleguy.opnsense.shaper_rule            | [Docs](https://opnsense.ansibleguy.net/modules/shaper.html)                                             | unstable              |
| **Monit**           | ansibleguy.opnsense.monit_service          | [Docs](https://opnsense.ansibleguy.net/modules/monit.html)                                              | unstable              |
| **Monit**           | ansibleguy.opnsense.monit_alert            | [Docs](https://opnsense.ansibleguy.net/modules/monit.html)                                              | unstable              |
| **Monit**           | ansibleguy.opnsense.monit_test             | [Docs](https://opnsense.ansibleguy.net/modules/monit.html)                                              | unstable              |
| **WireGuard**       | ansibleguy.opnsense.wireguard_server       | [Docs](https://opnsense.ansibleguy.net/modules/wireguard.html)                                          | unstable              |
| **WireGuard**       | ansibleguy.opnsense.wireguard_peer         | [Docs](https://opnsense.ansibleguy.net/modules/wireguard.html)                                          | unstable              |
| **WireGuard**       | ansibleguy.opnsense.wireguard_show         | [Docs](https://opnsense.ansibleguy.net/modules/wireguard.html)                                          | unstable              |
| **WireGuard**       | ansibleguy.opnsense.wireguard_general      | [Docs](https://opnsense.ansibleguy.net/modules/wireguard.html)                                          | unstable              |
| **Interfaces**      | ansibleguy.opnsense.interface_vlan         | [Docs](https://opnsense.ansibleguy.net/modules/interface.html)                                          | unstable              |
| **Interfaces**      | ansibleguy.opnsense.interface_vxlan        | [Docs](https://opnsense.ansibleguy.net/modules/interface.html)                                          | unstable              |
| **Interfaces**      | ansibleguy.opnsense.interface_vip          | [Docs](https://opnsense.ansibleguy.net/modules/interface.html)                                          | development (_V23.1_) |
| **NAT**             | ansibleguy.opnsense.source_nat             | [Docs](https://opnsense.ansibleguy.net/modules/source_nat.html)                                         | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_diagnostic         | [Docs](https://opnsense.ansibleguy.net/modules/frr_diagnostic.html)                                     | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_bfd_general        | [Docs](https://opnsense.ansibleguy.net/modules/frr_bfd.html#ansibleguy-opnsense-frr-bfd-general)        | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_bfd_neighbor       | [Docs](https://opnsense.ansibleguy.net/modules/frr_bfd.html#ansibleguy-opnsense-frr-bfd-neighbor)       | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_bgp_general        | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-general)        | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_bgp_neighbor       | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-neighbor)       | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_bgp_prefix_list    | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-prefix-list)    | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_bgp_route_map      | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-route-map)      | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_bgp_community_list | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-community-list) | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_bgp_as_path        | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-as-path)        | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_ospf_general       | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-general)      | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_ospf_prefix_list   | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-prefix-list)  | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_ospf_interface     | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-interface)    | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_ospf_network       | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-network)      | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_ospf3_general      | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-general)     | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_ospf3_interface    | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-interface)   | unstable              |
| **Dynamic Routing** | ansibleguy.opnsense.frr_rip                | [Docs](https://opnsense.ansibleguy.net/modules/frr_rip.html)                                            | unstable              |
| **DNS**             | ansibleguy.opnsense.bind_general           | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-general)              | unstable              |
| **DNS**             | ansibleguy.opnsense.bind_blocklist         | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-blocklist)            | unstable              |
| **DNS**             | ansibleguy.opnsense.bind_acl               | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-acl)                  | unstable              |
| **DNS**             | ansibleguy.opnsense.bind_domain            | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-domain)               | unstable              |
| **DNS**             | ansibleguy.opnsense.bind_record            | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-record)               | unstable              |
| **DNS**             | ansibleguy.opnsense.bind_record_multi      | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-record-multi)         | unstable              |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_general       | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id2)                                       | unstable              |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_cache         | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id3)                                       | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_parent        | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id4)                                       | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_traffic       | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id5)                                       | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_forward       | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id7)                                       | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_acl           | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id8)                                       | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_icap          | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id9)                                       | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_auth          | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id10)                                      | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_remote_acl    | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id12)                                      | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_pac_proxy     | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id14)                                      | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_pac_match     | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id15)                                      | unstable           |
| **Web Proxy**       | ansibleguy.opnsense.webproxy_pac_rule      | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id18)                                      | unstable           |


### Roadmap

**Core API**:

- [IDS](https://docs.opnsense.org/development/api/core/ids.html)
- [Diagnostics](https://docs.opnsense.org/development/api/core/diagnostics.html)
- [Interface - Loopback](https://docs.opnsense.org/development/api/core/interfaces.html)
- [IPSec](https://docs.opnsense.org/development/api/core/ipsec.html) => [waiting for API](https://github.com/opnsense/core/pull/6187#issuecomment-1356263118)

**Plugins API**:

- [Zabbix Agent](https://docs.opnsense.org/development/api/plugins/zabbixagent.html)
- [STunnel](https://docs.opnsense.org/development/api/plugins/stunnel.html)
- [Backup](https://docs.opnsense.org/development/api/plugins/backup.html)
- [FreeRadius](https://docs.opnsense.org/development/api/plugins/freeradius.html)
- [Zabbix Proxy](https://docs.opnsense.org/development/api/plugins/zabbixproxy.html)
