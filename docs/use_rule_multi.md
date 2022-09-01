# OPNSense - Rule module

**STATE**: testing

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/rule_multi.yml) | [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/rule_purge.yml)

**API DOCS**: [Plugins - Firewall](https://docs.opnsense.org/development/api/plugins/firewall.html)

## Info

For basic info, limitations and must-know to the rule-handling see the [rule](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md) module!

## Multi

- Each rule has the attributes as defined in the [rule](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md) module

- To ensure valid configuration - the attributes of each rule get verified using ansible's built-in verifier

## Usage

The 'rule_multi' module is meant to manage dictionaries of rules.

You could either invoke this module:

- once for all rules
- once per logical grouping of rules (_see [grouping example](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md#logical_grouping)_)


## Examples

### Basics

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.rule_multi:
      firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
      api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"
      match_fields: ['description']
      key_field: 'description'  # rule-field that is used as key of the 'rules' dictionary

    ansibleguy.opnsense.rule_list:
      firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
      api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

    ansibleguy.opnsense.alias_purge:
      firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
      api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

  tasks:
    - name: Changing
      ansibleguy.opnsense.rule_multi:
        rules:
          test1:
            source_net: '192.168.1.0/24'
            destination_invert: true
            destination_net: '10.1.0.0/8'
            action: 'block'
          test2:
            source_net: '192.168.0.0/16'
            destination_net: '10.156.10.0/24'
            destination_port: 8080
            protocol: 'TCP'
            interface: ['lan', 'opt1']
          # alternatively using shorter parameters
          test3:
            src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
            int: 'wan'
            action: 'block'
          test4:
            src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
            int: 'wan'
            action: 'block'
            ip_proto: 'inet6'
            state: 'absent'

    - name: Pulling existing rules
      ansibleguy.opnsense.rule_list:
      register: existing_rules

    - name: Printing rules
      ansible.builtin.debug:
        var: existing_rules.rules

    - name: Purging all non-configured rules
      ansibleguy.opnsense.rule_purge:
        aliases: {...}
        # action: 'disable'  # default = remove

    - name: Purging allow-rules on interface opt2 that use IPv4
      ansibleguy.opnsense.rule_purge:
        filters:  # filtering rules to purge by rule-parameters
          ip_protocol: 'inet'
          action: 'allow'
          interface: ['opt2']
        # filter_invert: true  # purge all non-port rules
```

### Options

You can also override all rule parameters as needed.

```yaml
- name: Changing
  ansibleguy.opnsense.rule_multi:
    rules: {...}

    # set parameters and/or states to all rules
    override:
      interface: ['lan', 'opt1', 'opt2']
      log: true

    state: 'absent'
    enabled: false

    # or set default values for all rules (override the built-in default values)    
    defaults:
      action: 'block'
      sequence: 50
```

To simplify the modules usage and config - you can also use shorter parameter aliases.

```yaml
- name: Changing
  ansibleguy.opnsense.rule_multi:
    rules:
      test1:
        src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
        int: 'wan'
        action: 'block'
      test2:
        src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
        int: 'wan'
        action: 'block'
        ip_proto: 'inet6'
        state: 'absent'
      test3:
        s: '192.168.0.0/16'  # source
        d: '10.81.53.0/24'  # destination
        dp: 443  # destination_port
        p: 'TCP'  # protocol
        i: ['lan', 'opt1']  # interface
        en: false  # enabled
```

### Troubleshooting

- info
- debug overall
- debug per rule

To simplify troubleshooting of bad configuration there are some troubleshooting parameters available.


```yaml
- name: Changing
  ansibleguy.opnsense.rule_multi:
    rules: {...}
    fail_verification: true  # if the module should fail if one rule has a bad config (default behaviour)
    output_info: true  # to output information of processed rules => also shown if the task is set to 'no_log: true'
    debug: true  # output verbose information about requests and processing
```


### Logical grouping

This example shows an option how to manage complexer rule-sets and/or template rules across multiple sites.

Basically we are abstracting the rule-set into interface-groups (_I'll call them zones_)

```yaml
to be done
```
