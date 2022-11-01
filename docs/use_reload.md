# OPNSense - Reload module

**STATE**: stable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/reload.yml)

## Info

This module can reload the running/loaded configuration for a specified part of the OPNSense system.

Most modules of this collection will automatically reload its relevant running config on change - but you can speed up mass-management of items when disabling reload on single module-calls (_reload: false_), and do it afterward using THIS module.

Alternatively you can use the [service module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_service.md) with action 'reload' if you like it better.

## Definition

| Parameter | Type   | Required | Default value | Comment                                                                                                                        |
|:----------|:-------|:---------|:--------------|:-------------------------------------------------------------------------------------------------------------------------------|
| target      | string | true     | -             | What part of the running config should be reloaded. One of: 'alias', 'route', 'cron', 'unbound', 'syslog', 'ipsec', 'shaper', 'monit', 'wireguard', 'interface_vlan', 'interface_vxlan', 'frr' |

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

### Practical

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.reload:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.route:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.unbound_host:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Adding routes
      ansibleguy.opnsense.route:
        network: "{{ item.nw }}"
        gateway: "{{ item.gw }}"
        reload: false
      loop:
        - {nw: '10.206.0.0/16', gw: 'VPN_GW'}
        - {nw: '10.67.0.0/16', gw: 'VPN2_GW'}

    - name: Adding DNS overrides
      ansibleguy.opnsense.unbound_host:
        hostname: "{{ item.host }}"
        domain: 'opnsense.template.ansibleguy.net'
        value: "{{ item.value }}"
        reload: false
      loop:
        - {host: 'a', value: '192.168.0.1'}
        - {host: 'd', value: '192.168.0.5'}

    - name: Reloading
      ansibleguy.opnsense.reload:
        target: "{{ item }}"
      loop:
        - 'route'
        - 'unbound'
```

