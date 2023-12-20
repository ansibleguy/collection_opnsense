# DNS - Unbound General

**STATE**: stable

**TESTS**: [unbound_general](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/unbound_general.yml)

**API Docs**: [Core - Unbound](https://docs.opnsense.org/development/api/core/unbound.html)

**Service Docs**: [Unbound DNS](https://docs.opnsense.org/manual/unbound.html)

## Requirements

This module requires OPNsense 23.7 or later.

## Info

**WARNING:** Unbound service actions like :code:`reload` can take very long (>90s). Please be aware of the **possible downtime**!


You may also need to increase the module `timeout`.


## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/use_basic.md#definition)

### ansibleguy.opnsense.unbound_general

| Parameter                     | Type    | Required | Default value | Aliases | Comment                                                                                                                                                                                                                                                                                  |
|:------------------------------|:--------|:---------|:--------------|:--------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| enabled                       | bool    | false    | true          | -       | En- or disable the Unbound DNS service                                                                                                                                                                                                                                                   |
| port                          | int     | false    | 53            | -       | The TCP/UDP port used for responding to DNS queries                                                                                                                                                                                                                                      |
| interfaces                    | list    | false    | -             | -       | The interface(s) used for responding to queries from clients                                                                                                                                                                                                                             |
| dnssec                        | bool    | false    | false         | -       | En- or disable DNSSEC                                                                                                                                                                                                                                                                    |
| dns64                         | bool    | false    | false         | -       | En- or disable to synthesize AAAA records from A records if no actual AAAA records are present                                                                                                                                                                                           |
| dns64_prefix                  | string  | false    | '64:ff9b::/96'  | -       | The DNS64 prefix                                                                                                                                                                                                                                                                         |
| aaaa_only_mode                | bool    | false    | false         | -       | En- or disable to remove all A records from the answer section of all responses                                                                                                                                                                                                          |
| register_dhcp_leases          | bool    | false    | false         | -       | En- or disable to register machines that specify their hostname when requesting a DHCP lease                                                                                                                                                                                             |
| dhcp_domain                   | string  | false    | -             | -       | The default domain name to use for DHCP lease registration                                                                                                                                                                                                                               |
| register_dhcp_static_mappings | bool    | false    | false         | -       | En- or disable to register DHCP static mappings                                                                                                                                                                                                                                          |
| register_ipv6_link_local      | bool    | false    | true          | -       | En- or disable to register IPv6 link-local addresses                                                                                                                                                                                                                                     |
| register_system_records       | bool    | false    | true          | -       | En- or disable to generate A/AAAA records for the configured listen interfaces                                                                                                                                                                                                           |
| txt_records                   | bool    | false    | false         | txt     | En- or disable to create TXT record for descriptions associated with Host entries and DHCP Static mappings                                                                                                                                                                               |
| flush_dns_cache               | bool    | false    | false         | -       | En- or disable to flush the DNS cache during each daemon reload                                                                                                                                                                                                                          |
| local_zone_type               | string  | false    | 'transparant'   | -       | The local zone type used for the system domain. One of: 'transparent', 'always_nxdomain', 'always_refuse', 'always_transparent', 'deny', 'inform', 'inform_deny', 'nodefault', 'refuse', 'static', 'typetransparent'                                                                     |
| outgoing_interfaces           | list    | false    | -             | -       | The interface(s) that Unbound will use to send queries to authoritative servers and receive their replies                                                                                                                                                                                |
| wpad                          | bool    | false    | false         | -       | En- or disable to automatically add CNAME records for the WPAD host of all configured domains as well as overrides for TXT records for domains                                                                                                                                           |
| reload                        | boolean | false    | true          | -       | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/use_reload.md). |

## Examples

### ansibleguy.opnsense.unbound_general

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.unbound_general:
        # enabled: true
        # port: 53
        # interfaces: ''
        # dnssec: false
        # dns64: false
        # dns64_prefix: '64:ff9b::/96'
        # aaaa_only_mode: false
        # register_dhcp_leases: false
        # dhcp_domain: ''
        # register_dhcp_static_mappings: false
        # register_ipv6_link_local: true
        # register_system_records: true
        # txt_records: false
        # flush_dns_cache: false
        # local_zone_type: 'transparent'
        # outgoing_interfaces: ''
        # wpad: false
        # reload: true


    - name: Enabling Unbound
      ansibleguy.opnsense.unbound_general:
        enabled: true
        port: 53
        interfaces: ['lan']
        local_zone_type: 'transparent'
```
