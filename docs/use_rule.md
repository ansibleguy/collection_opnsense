# OPNSense - Rule module

**STATE**: testing

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/rule.yml)

**API DOCS**: [Plugins - Firewall](https://docs.opnsense.org/development/api/plugins/firewall.html)

## Prerequisites

You need to install the following plugin as OPNSense has no core-api for managing its firewall rules:
```
os-firewall
```

You can also install it using the [package module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md).

## Limitations

This plugin has some major limitations you need to know of:

* it does not work with aliases
* every rule can only have one

  * source network
  * destination network
  * ip-protocol
  * protocol

Here's a forum topic regarding these limitations: [LINK](https://forum.opnsense.org/index.php?topic=30077.0)

## Info

You can prevent lockout-situations using the savepoint systems:

- [Firewall - Savepoint](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_savepoint.md)

These rules are shown in the separate WEB-UI table.

Menu: 'Firewall - Automation - Filter'

## Usage

First you will have to know about **rule-matching**.

The module somehow needs to link the configured and existing rules to manage them.

You can modify how this matching is done by setting the 'match_fields' parameter!

It is **recommended** to use/set **unique identifiers** like 'description' to make sure rules can be matched without overlapping.

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.multi_alias:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
  
  tasks:
    - name: Test
      ansibleguy.opnsense.rule:
        source_net: '192.168.0.0/24'
        destination_net: '192.168.10.0/24'
        destination_port: 443
        protocol: 'TCP'  # for options see the WEB-UI
        description: 'Generic test'
        # match_fields: ['ip_protocol', 'source_invert', 'source_net', 'description']
        # sequence: 1
        # action: 'pass'
        # interface: 'lan'
        # direction: 'in
        # ip_protocol: 'inet' or 'inet6'
        # source_invert: false
        # source_port: ''
        # destination_invert: false
        # log: true
        # gateway: 'LAN_GW'
        # state: 'present'
        # enabled: true
        # debug: true
```
