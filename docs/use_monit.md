# OPNSense - Monit modules

**STATE**: testing/development

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/monit.yml)

**API DOCS**: [Core - Monit](https://docs.opnsense.org/development/api/core/monit.html)

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

| Parameter    | Type            | Required | Default value         | Aliases | Comment |
|:-------------|:----------------|:---------|:----------------------|:--------|:--------|
| -            | -               | -        | -                     | -       | -       |

## Usage

-
## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.monit_service:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'monit_service'

  tasks:
    - name: Example      
      ansibleguy.opnsense.monit_service:
        description: 'test1'
        name: 'test'
        type: 'network'
        address: '192.168.0.1'
```
