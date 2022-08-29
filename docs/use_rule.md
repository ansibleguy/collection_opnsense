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

This plugin has some limitations you need to know of:

* ports don't support aliases
* each of these parameters only takes ONE value per rule:
  * port
  * protocol
  * ip-protocol (_IPv4/IPv6_)
  * interface (_any is not an option_)
  * direction
* the ruleset managed by this plugin is SEPARATE from the default WEB-UI rules (_Firewall - Rules_) - combined usage might bring complications

## Info

### Savepoint

You can prevent lockout-situations using the savepoint systems:

- [Firewall - Savepoint](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_savepoint.md)

### Mass-Manage

If you want to mass-manage rules - take a look at the [multi_rule](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_multi_rule.md) module. It is scales better for that use-case!

### Web-UI

These rules are shown in the separate WEB-UI table.

Menu: 'Firewall - Automation - Filter'

## Usage

First you will have to know about **rule-matching**.

The module somehow needs to link the configured and existing rules to manage them.

Need to set how this matching is done by setting the 'match_fields' parameter!

It is **recommended** to use/set **unique identifiers** like 'description' to make sure rules can be matched without overlapping.


### Basic

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.rule:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.rule_list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.rule:
        source_net: '192.168.0.0/24'  # host, network, alias or 'any'
        destination_net: '192.168.10.0/24'
        destination_port: 443  # alias not supported, leave unset for 'any'
        protocol: 'TCP'  # for options see the WEB-UI
        description: 'Generic test'
        match_fields: ['description']
        # sequence: 1
        # action: 'pass'
        # quick: true
        # interface: 'lan'
        # direction: 'in'
        # ip_protocol: 'inet' or 'inet6'
        # source_invert: false
        # source_port: ''
        # destination_invert: false
        # log: true
        # gateway: 'LAN_GW'
        # state: 'present'
        # enabled: true
        # debug: true

    - name: Listing
      ansibleguy.opnsense.rule_list:
      register: existing_rules

    - name: Printing rules
      ansible.bultin.debug:
        var: existing_rules.rules
```

### With inventory config

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.rule:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      match_fields: ['description']  # setting description as unique-id field

  # you may want to configure your rules inside the inventory
  vars:
    rules:
      wan_deny_tor_exit_nodes_ipv4:
        src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
        int: 'wan'
        action: 'deny'
      wan_deny_tor_exit_nodes_ipv6:
        src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
        int: 'wan'
        action: 'deny'
        ip_proto: 'inet6'
      lan_to_dmz_https:
        src: 'LAN_net'
        dest: 'DMZ_net'
        dest_port: 443
      lan_to_dmz_http:
        src: 'LAN_net'
        dest: 'DMZ_net'
        dest_port: 80
      internal_to_inet_http:
        src: '172.16.0.0/16'
        dest_invert: true
        dest: 'bogons'
        dest_port: 80
      internal_to_inet_https:
        src: '172.16.0.0/16'
        dest_invert: true
        dest: 'bogons'
        dest_port: 443

  tasks:
    - name: Test
      ansibleguy.opnsense.rule:
        description: "{{ rule_id }}"

        action: "{{ rule.action | default(omit) }}"
        interface: "{{ rule.int | default(omit) }}"
        direction: "{{ rule.dir | default(omit) }}"
        ip_protocol: "{{ rule.ip_proto | default(omit) }}"
        protocol: "{{ rule.proto | default(omit) }}"

        source_invert: "{{ rule.src_invert | default(omit) }}"
        source_net: "{{ rule.src | default(omit) }}"
        source_port: "{{ rule.src_port | default(omit) }}"
        destination_invert: "{{ rule.dest_invert | default(omit) }}"
        destination_net: "{{ rule.dest | default(omit) }}"
        destination_port: "{{ rule.dest_port | default(omit) }}"
        
        sequence: "{{ rule.seq | default(omit) }}"
        quick: "{{ rule.quick | default(omit) }}"
        log: "{{ rule.log | default(omit) }}"
        gateway: "{{ rule.gw | default(omit) }}"
        state: "{{ rule.state | default(omit) }}"
        enabled: "{{ rule.enabled | default(omit) }}"
        # debug: "{{ rule.debug | default(omit) }}"

      vars:
        rule: "{{ rule_item.value }}"
        rule_id: "{{ rule_item.key }}"

      loop_control:
        loop_var: rule_item
      with_dict: "{{ rules }}"

```

### Purging

If you want to delete all existing rules that are **NOT CONFIGURED**.

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.rule_list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.rule:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      match_fields: ['description']

  vars:
    rules: {...}

  tasks:
    - name: Pulling existing rules
      ansibleguy.opnsense.rule_list:
      register: existing_rules

    - name: Purging unconfigured rules
      ansibleguy.opnsense.rule:
        state: 'absent'
        description: "{{ existing_rule_id }}"

      when: existing_rule_id not in rules
      
      vars:
        existing_rule_id: "{{ existing_rule_item.value.description }}"
      
      loop_control:
        loop_var: existing_rule_item
      with_dict: "{{ existing_rules }}"
```
