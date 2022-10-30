# OPNSense - FRR BFD module

**STATE**: unstable

**TESTS**: [frr_bfd](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_bfd.yml)

**API DOCS**: [Plugins - Quagga](https://docs.opnsense.org/development/api/plugins/quagga.html)

**BASE DOCS**: [Dynamic Routing](https://docs.opnsense.org/manual/dynamic_routing.html)

**FRR DOCS**: [FRRouting](https://docs.frrouting.org/) (_make sure you are looking at the current OPNSense package version!_)

## Prerequisites

You need to install the FRR plugin:
```
os-frr
```

You can also install it using the [package module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md).

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

### ansibleguy.opnsense.frr_bfd

| Parameter    | Type            | Required | Default value         | Aliases                          | Comment                                                                                                            |
|:-------------|:----------------|:---------|:----------------------|:---------------------------------|:-------------------------------------------------------------------------------------------------------------------|
| ip           | string          | true     | -                     | neighbor, address, peer_ip, peer | The neighbor IP or IP-range to manage. This field will be used to match existing entries with the provided config! |
| description  | string          | false    | -                     | desc                             | Optional description for the neighbor                                                                              |                                                                                                                                                  |


## Examples

### ansibleguy.opnsense.frr_bfd

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_bfd:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_bfd'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_bfd:
        ip: '10.0.0.1'
        # description: 'test1'
        # enabled: true
        # debug: false
        # state: 'present'
        # reload: true

    - name: Adding neighbor
      ansibleguy.opnsense.frr_bfd:
        ip: '10.0.0.1'
        description: 'test2'

    - name: Disabling neighbor
      ansibleguy.opnsense.frr_bfd:
        ip: '10.0.0.1'
        description: 'test2'
        enabled: false

    - name: Listing neighbors
      ansibleguy.opnsense.list:
      #  target: 'frr_bfd'
      register: existing_entries

    - name: Printing neighbors
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing neighbor 'test3'
      ansibleguy.opnsense.frr_bfd:
        ip: '10.0.0.1'
        state: 'absent'
```
