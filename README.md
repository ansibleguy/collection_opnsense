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
* implement additional API endpoints => see [development guide](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/develop.md)
* test unstable modules and report bugs/errors

----

## Requirements

The [httpx python module](https://www.python-httpx.org/) is used for API communications!

```bash
python3 -m pip install httpx
```

The [validators python module](https://validators.readthedocs.io/) is used to validate user-provided data on the client-side.

```bash
python3 -m pip install validators
```

Then - install the collection itself:

```bash
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git

# or for easier development

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


| Function                | Module                                     | Usage                                                                                                | State    |
|:------------------------|:-------------------------------------------|:-----------------------------------------------------------------------------------------------------|:---------|
| **Base**                | ansibleguy.opnsense.list                   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_list.md)               | stable   |
| **Base**                | ansibleguy.opnsense.reload                 | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md)             | stable   |
| **Base**                | ansibleguy.opnsense.service                | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_service.md)            | stable |
| **Alias**               | ansibleguy.opnsense.alias                  | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md)              | stable   | 
| **Alias**               | ansibleguy.opnsense.alias_multi            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md)        | stable   |
| **Alias**               | ansibleguy.opnsense.alias_purge            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md)        | unstable   |
| **Rules**               | ansibleguy.opnsense.rule                   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md)               | unstable |
| **Rules**               | ansibleguy.opnsense.rule_multi             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)         | unstable |
| **Rules**               | ansibleguy.opnsense.rule_purge             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)         | unstable |
| **Savepoints**          | ansibleguy.opnsense.savepoint              | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_savepoint.md)          | unstable |
| **Packages**            | ansibleguy.opnsense.package                | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md)            | stable   |
| **System**              | ansibleguy.opnsense.system                 | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_system.md)             | unstable |
| **Cron-Jobs**           | ansibleguy.opnsense.cron                   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_cron.md)               | unstable |
| **Routes**              | ansibleguy.opnsense.route                  | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_route.md)              | unstable |
| **DNS**                 | ansibleguy.opnsense.unbound_forward        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_forwarding.md) | stable   |
| **DNS**                 | ansibleguy.opnsense.unbound_dot            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_dot.md)        | stable   |
| **DNS**                 | ansibleguy.opnsense.unbound_host           | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host.md)       | stable   |
| **DNS**                 | ansibleguy.opnsense.unbound_domain         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_domain.md)     | stable |
| **DNS**                 | ansibleguy.opnsense.unbound_host_alias     | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host_alias.md) | unstable |
| **Syslog**              | ansibleguy.opnsense.syslog                 | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_syslog.md)             | stable   |
| **IPSec**               | ansibleguy.opnsense.ipsec_cert             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_ipsec.md)              | unstable |
| **Traffic Shaper**      | ansibleguy.opnsense.shaper_pipe            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_shaper.md)             | unstable |
| **Traffic Shaper**      | ansibleguy.opnsense.shaper_queue           | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_shaper.md)             | unstable |
| **Traffic Shaper**      | ansibleguy.opnsense.shaper_rule            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_shaper.md)             | unstable |
| **Monit**               | ansibleguy.opnsense.monit_service          | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md)              | unstable |
| **Monit**               | ansibleguy.opnsense.monit_alert            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md)              | unstable |
| **Monit**               | ansibleguy.opnsense.monit_test             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md)              | unstable |
| **WireGuard**           | ansibleguy.opnsense.wireguard_server       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md)          | unstable |
| **WireGuard**           | ansibleguy.opnsense.wireguard_peer         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md)          | unstable |
| **WireGuard**           | ansibleguy.opnsense.wireguard_show         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md)          | unstable |
| **WireGuard**           | ansibleguy.opnsense.wireguard_general      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md)          | unstable |
| **Interfaces**          | ansibleguy.opnsense.interface_vlan         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_interface.md)          | unstable |
| **Interfaces**          | ansibleguy.opnsense.interface_vxlan        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_interface.md)          | unstable |
| **NAT**                 | ansibleguy.opnsense.source_nat             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_source_nat.md)         | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_diagnostic         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_diagnostic.md)     | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_bfd_general        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bfd.md)            | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_bfd_neighbor       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bfd.md)            | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_bgp_general        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_bgp_neighbor       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_bgp_prefix_list    | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_bgp_route_map      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_bgp_community_list | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_bgp_as_path        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_ospf_general       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_ospf_prefix_list   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_ospf_interface     | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_ospf_network       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_ospf3_general      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_ospf3_interface    | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**     | ansibleguy.opnsense.frr_rip                | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_rip.md)            | unstable |
| **DNS**                 | ansibleguy.opnsense.bind_general           | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md)               | unstable |
| **DNS**                 | ansibleguy.opnsense.bind_blocklist         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md)               | unstable |
| **DNS**                 | ansibleguy.opnsense.bind_acl               | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md)               | unstable |
| **DNS**                 | ansibleguy.opnsense.bind_domain            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md)               | unstable |
| **DNS**                 | ansibleguy.opnsense.bind_record            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md)               | unstable |
| **DNS**                 | ansibleguy.opnsense.bind_record_multi      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md)               | unstable |


### Roadmap

**Core API**:

- [Proxy](https://docs.opnsense.org/development/api/core/proxy.html)
- [IDS](https://docs.opnsense.org/development/api/core/ids.html)
- [Diagnostics](https://docs.opnsense.org/development/api/core/diagnostics.html)
- [IPSec](https://docs.opnsense.org/development/api/core/ipsec.html) => [waiting for API](https://github.com/opnsense/core/pull/6187#issuecomment-1356263118)

**Plugins API**:

- [Zabbix Agent](https://docs.opnsense.org/development/api/plugins/zabbixagent.html)
- [STunnel](https://docs.opnsense.org/development/api/plugins/stunnel.html)
- [Backup](https://docs.opnsense.org/development/api/plugins/backup.html)
- [FreeRadius](https://docs.opnsense.org/development/api/plugins/freeradius.html)
- [Zabbix Proxy](https://docs.opnsense.org/development/api/plugins/zabbixproxy.html)
