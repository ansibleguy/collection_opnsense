# OPNSense - Source-NAT module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/source_nat.yml)

**API DOCS**: [Plugins - Firewall](https://docs.opnsense.org/development/api/plugins/firewall.html)

**BASE DOCS**: [Source NAT](https://docs.opnsense.org/manual/nat.html#outbound)

## Prerequisites

You need to install the following plugin as OPNSense has no core-api for managing its firewall rules:
```
os-firewall
```

You can also install it using the [package module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md).

## Limitations

This plugin has some limitations you need to know of:

* ports don't support aliases
* each of these parameters only takes ONE value per rule:
  * port
  * protocol (_or 'any'; 'TCP/UDP' is NOT valid_)
  * ip-protocol (_IPv4/IPv6_)
* the ruleset managed by this plugin is SEPARATE from the default WEB-UI rules (_Firewall - NAT - Outbound_) - combined usage might bring complications
* interfaces must be provided as used in the network config (_p.e. 'opt1' instead of 'DMZ'_)
  * per example see menu: 'Interface - Assignments - Interface ID (in brackets)'
  * this brings problems if the interface-names are not the same on both nodes when using HA-setups


## Info

### Savepoint

You can prevent lockout-situations using the savepoint systems:

- [Firewall - Savepoint](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_savepoint.md)

### Web-UI

These rules are shown in the separate WEB-UI table.

Menu: 'Firewall - Automation - Source NAT'

## Definition

| Parameter          | Type    | Required | Default value | Aliases                | Comment                                                                                                                                                                                                                                                                                                                                                                                     |
|:-------------------|:--------|:---------|:--------------|:-----------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields       | list  | true     | -             | -                      | Fields that are used to match configured rules with the running config - if any of those fields are changed, the module will think it's a new rule. At least one of: 'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net', 'destination_port', 'gateway', 'description', 'uuid' |
| sequence           | int     | false    | 1             | seq                    | Sequence for rule processing, Integer between 1 and 1000000                                                                                                                                                                                                                                                                                                                                 |
| interface          | string    | false for deletion, else true    | -             | i, int                 | The interface to match this rule on                                                                                                                                                                                                                                                                                                                                                         |
| ip_protocol        | string  | false    | 'inet'        | ipp, ip_proto          | IP protocol to match. One of: 'inet', 'inet6' (_IPv4 = 'inet', IPv6 = 'inet6'_)                                                                                                                                                                                                                                                                                                             |
| protocol           | string  | false    | 'any'         | p, proto               | Protocol like 'TCP', 'UDP', 'ICMP' and so on. For options see the WEB-UI. 'TCP/UDP' is NOT valid!                                                                                                                                                                                                                                                                                           |
| source_invert      | boolean | false    | false         | si, src_inv, src_not   | Inverted matching of the source                                                                                                                                                                                                                                                                                                                                                             |
| source_net         | string | false    | 'any'         | s, src, source         | Host, network, alias or 'any'                                                                                                                                                                                                                                                                                                                                                               |
| source_port        | string | false    | -             | sp, src_port           | Leave empty to allow all, alias not supported                                                                                                                                                                                                                                                                                                                                               |
| destination_invert | boolean | false    | false         | di, dest_inv, dest_not | Inverted matching of the destination                                                                                                                                                                                                                                                                                                                                                        |
| destination_net    | string | false    | 'any'         | d, dest, destination   | Host, network, alias or 'any'                                                                                                                                                                                                                                                                                                                                                               |
| destination_port   | string | false    | -             | dp, dest_port          | Leave empty to allow all, alias not supported                                                                                                                                                                                                                                                                                                                                               |
| target             | string | false for deletion, else true    | -             | tgt, t                 | NAT translation target - Packets matching this rule will be mapped to the IP address given here. Host, network or alias                                                                                                                                                                                                                                                                     |
| target_port        | string | false    | -             | np, nat_port           |                                                                                                                                                                                                                                                                                                                                                                                             |
| log                | boolean  | false    | true          | l                      | If rule matches should be shown in the firewall logs                                                                                                                                                                                                                                                                                                                                        |
| description        | string  | false    | -             | desc                   | Description for the rule                                                                                                                                                                                                                                                                                                                                                                    |
| state              | string  | false    | 'present'     | st                     | State of the rule. One of: 'present', 'absent'                                                                                                                                                                                                                                                                                                                                              |
| enabled            | boolean  | false    | true          | en                     | If the rule should be en- or disabled                                                                                                                                                                                                                                                                                                                                                       |
| uuid               | string  | false    | -             | -                      | Optionally you can supply the uuid of an existing rule                                                                                                                                                                                                                                                                                                                                      |


For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

## Usage

First you will have to know about **rule-matching**.

The module somehow needs to link the configured and existing rules to manage them.

You need to set how this matching is done by setting the 'match_fields' parameter!

It is **recommended** to use/set **unique identifiers** like 'description' to make sure rules can be matched without overlapping.

You could also use the UUID of existing rules as ID - but you would have to pull (_list_) and configure those manually. 


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.source_nat:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      match_fields: ['description']

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'source_nat'

  tasks:
    - name: Example
      ansibleguy.opnsense.source_nat:
        description: 'example'
        match_fields: ['description']
        target: '192.168.0.1'
        interface: 'opt1'
        # sequence: 1
        # ip_protocol: 'inet'
        # protocol: 'any'
        # source_invert: false
        # source_net: 'any'
        # source_port: 'any'
        # destination_invert: false
        # destination_net: 'any'
        # destination_port: 'any'
        # destination_port: 'any'
        # target_port: none
        # no_nat: false
        # log: true
        # enabled: true
        # debug: false
        # state: 'present'
        # reload: true

    - name: Adding rule
      ansibleguy.opnsense.source_nat:
        description: 'test1'
        source: '192.168.0.0/24'
        destination: '10.0.0.0/24'
        target: '10.0.0.1'
        interface: 'opt1'
        # match_fields: ['description']

    - name: Disabling rule
      ansibleguy.opnsense.source_nat:
        description: 'test1'
        source: '192.168.0.0/24'
        destination: '10.0.0.0/24'
        target: '10.0.0.1'
        interface: 'opt1'
        enabled: false
        # match_fields: ['description']

    - name: Listing peers
      ansibleguy.opnsense.list:
      #  target: 'source_nat'
      register: existing_entries

    - name: Printing
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing rule
      ansibleguy.opnsense.source_nat:
        description: 'test1'
        state: 'absent'
        # match_fields: ['description']
```
