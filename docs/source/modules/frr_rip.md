# FRR RIP

**STATE**: unstable

**TESTS**: [frr_rip](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_rip.yml)

**API Docs**: [Plugins - Quagga](https://docs.opnsense.org/development/api/plugins/quagga.html)

**Service Docs**: [Dynamic Routing](https://docs.opnsense.org/manual/dynamic_routing.html)

**FRR Docs**: [FRRouting](https://docs.frrouting.org/) (_make sure you are looking at the current OPNSense package version!_)

## Sponsoring

Thanks to [@telmich](https://github.com/telmich) for sponsoring the development of these modules!

## More FRR modules

* [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr.md)

## Prerequisites

You need to install the FRR plugin:
```
os-frr
```

You can also install it using the [package module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md).

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

### ansibleguy.opnsense.frr_rip

| Parameter | Type    | Required | Default value | Aliases            | Comment                                                                                                                                        |
|:----------|:--------|:---------|:--------------|:-------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| version   | integer | false    | 2             | v                  | RIP version. 1 or 2                                                                                                                            |
| metric    | integer | false    | -             | m                  | Default metric. Integer from 1 to 16                                                                                                           |                                                                                                                                                  |
| passive_ints    | list    | false    | -             | passive_interfaces | Select the interfaces, where no RIP packets should be sent to                                                                                  |                                                                                                                                                  |
| networks    | list    | false    | -             | nets               | Enter your networks in CIDR notation                                                                                                           |                                                                                                                                                  |
| redistribute    | list    | false    | -             | -                  | Select other routing sources, which should be redistributed to the other nodes. One or more of: 'bgp', 'ospf', 'connected', 'kernel', 'static' |                                                                                                                                                  |


## Examples

### ansibleguy.opnsense.frr_rip

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_rip:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_rip'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_rip:
        # version: 2
        # metric: 10
        # passive_ints: []
        # redistribute: []
        # networks: []
        # enabled: true

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_rip'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Enabling & Configuring RIP
      ansibleguy.opnsense.frr_rip:
        passive_ints: ['lan']
        redistribute: ['static']
        networks: ['10.0.10.0/24']
        enabled: true

    - name: Disabling RIP
      ansibleguy.opnsense.frr_rip:
        enabled: false
```
