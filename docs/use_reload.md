# OPNSense - Reload module

**STATE**: testing

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/reload.yml)

## Info

This module can reload the running/loaded configuration for a specified part of the OPNSense system.

Most modules of this collection will automatically reload its relevant running config on change - but you can speed up mass-management of items when disabling reload on single module-calls (_reload: false_), and do it afterward using THIS module.

## Definition

| Parameter | Type   | Required | Default value | Comment                                                                                           |
|:----------|:-------|:---------|:--------------|:--------------------------------------------------------------------------------------------------|
| target      | string | true     | -             | What part of the running config should be reloaded. One of: 'alias', 'rule', 'route', 'cron', 'unbound', 'syslog'                                      |

## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.reload:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Reloading aliases
      ansibleguy.opnsense.reload:
        target: 'alias'

    - name: Reloading routes
      ansibleguy.opnsense.reload:
        target: 'route'
```
