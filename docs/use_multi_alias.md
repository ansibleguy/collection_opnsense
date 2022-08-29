# OPNSense - Multi-Alias module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/multi_alias.yml)

**API DOCS**: [Core - Firewall](https://docs.opnsense.org/development/api/core/firewall.html)

This module allows you to manage multiple aliases.

It is faster than the 'alias' module as it reduces the needed api/http calls.

## Info

For more detailed information on what alias types are supported - see [the documentation](https://docs.opnsense.org/manual/aliases.html).

**Config**:

- Each alias has the attributes as defined in the [alias](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md) module

- To ensure valid configuration - the attributes of each alias get verified using ansible's built-in verifier


## Usage

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.multi_alias:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
  
  tasks:
    - name: Creation
      ansibleguy.opnsense.multi_alias:
        aliases:
          test1:
            content: '1.1.1.1'
          test2:
            content: ['1.1.1.1', '1.1.1.2']
            description: 'to be deleted'
          test3:
            type: 'network'
            content: '10.0.0.0/24'
            description: 'to be disabled'

    - name: Changes
      ansibleguy.opnsense.multi_alias:
        aliases:
          test1:
            content: ['1.1.1.3']
          test2:
            state: 'absent'
          test3:
            enabled: false

    - name: Change state of all
      ansibleguy.opnsense.multi_alias:
        aliases:
          test1:
          test3:
        state: 'absent'
        # enabled: true
```
