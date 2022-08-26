# OPNSense - Multi-Alias module

**STATE**: testing - but usable

This module allows you to manage multiple aliases.

It is faster than the 'alias' module as it reduces the needed api/http calls.

**Config**:

- Each alias has the attributes as defined in the [alias](https://github.com/ansibleguy/collection_opnsense/blob/stable/use_alias.md) module

- To ensure valid configuration - the attributes of each alias get verified using ansible's built-in verifier


```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.multi_alias:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
  
  tasks:
    - name: Example creation
      ansibleguy.opnsense.multi_alias:
        aliases:
          test1:
            content: ['1.1.1.1']
          test2:
            content: ['1.1.1.1']
            description: 'to be deleted'
          test3:
            type: 'network'
            content: ['10.0.0.0/24']
            description: 'to be disabled'

    - name: Example changes
      ansibleguy.opnsense.multi_alias:
        aliases:
          test1:
            content: ['1.1.1.2']
          test2:
            state: 'absent'
          test3:
            enabled: false
```
