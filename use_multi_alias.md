# OPNSense - Multi-Alias module

This module allows you to manage multiple aliases.

Each alias has the attributes as defined in the [alias](https://github.com/ansibleguy/collection_opnsense/blob/stable/use_multi_alias.md) module!

STATE: unstable

```yaml
- hosts: localhost
  tasks:
    - name: Example
      ansibleguy.opnsense.multi_alias:
        firewall: 'opnsense.template.ansibleguy.net'
        api_credential_file: '/home/guy/.secret/opn.key'
        aliases:
          test1:
            content: ['1.1.1.1']
          test2:
            state: 'absent'
```
