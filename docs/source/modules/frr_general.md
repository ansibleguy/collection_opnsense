# FRR General

**STATE**: stable

**TESTS**: [frr_general](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/frr_general.yml)

**API Docs**: [Plugins - Quagga](https://docs.opnsense.org/development/api/plugins/quagga.html)

**Service Docs**: [Dynamic Routing](https://docs.opnsense.org/manual/dynamic_routing.html)

**FRR Docs**: [FRRouting](https://docs.frrouting.org/) (_make sure you are looking at the current OPNSense package version!_)

## Prerequisites

You need to install the FRR plugin:
```
os-frr
```

You can also install it using the [package module](https://opnsense.ansibleguy.net/en/latest/modules/package.html).

## Definition

For basic parameters see: [Basics](https://opnsense.ansibleguy.net/en/latest/usage/2_basic.html)

### ansibleguy.opnsense.frr_general

| Parameter | Type   | Required | Default value               | Aliases       | Comment                                                                                                                                      |
|:----------|:-------|:---------|:----------------------------|:--------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| enabled   | bool   | false     | true                        | -             | En- or disable the FRR service                                                                                                               |
| profile   | string          | false    | 'traditional'                            | -             | One of: 'traditional', 'datacenter'. The 'datacenter' profile is more aggressive. Please refer to the FRR documentation for more information |
| log      | bool   | false     | true                        | logging              | En- or disable (syslog) logging                                                                                                              |
| log_level   | string          | false    | 'notifications'             | -             | One of: 'critical', 'emergencies', 'errors', 'alerts', 'warnings', 'notifications', 'informational', 'debugging'.                            |
| carp      | bool   | false     | false                       | carp_failover | Will activate the routing service only on the primary device                                                                                 |
| snmp_agentx      | bool   | false     | false                       | -             | En- or disable support for Net-SNMP AgentX                                                                                                   |


## Examples

### ansibleguy.opnsense.frr_general

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_general:
        # enabled: true
        # profile: 'traditional'
        # log: true
        # log_level: 'notifications'
        # snmp_agentx: false
        # carp: false

    - name: Enabling FRR
      ansibleguy.opnsense.frr_general:
        enabled: true
        profile: 'traditional'
        log: true
        log_level: 'notifications'
```
