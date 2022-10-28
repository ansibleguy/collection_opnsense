# OPNSense - FRR module

**STATE**: unstable

**TESTS**: [frr_bfd](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_bfd.yml)

**API DOCS**: [Plugins - Quagga](https://docs.opnsense.org/development/api/plugins/quagga.html)

**BASE DOCS**: [Dynamic Routing](https://docs.opnsense.org/manual/dynamic_routing.html)

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

### ansibleguy.opnsense.frr_bgp_general

| Parameter    | Type    | Required | Default value         | Aliases   | Comment                                                                                                                                                                                                                   |
|:-------------|:--------|:---------|:----------------------|:----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| as_number           | string  | true     | -                     | as, as_nr | BGP AS-Number                                                                                                                                                                                                             |
| id  | string  | false    | -                     | router_id | In some cases it might be clearer to set a fixed router-id. (_4-byte field/IPv4 Address_)                                                                                                                                 |                                                                                                                                                  |
| graceful  | boolean | false    | -                     | -         | BGP graceful restart functionality as defined in RFC-4724 defines the mechanisms that allows BGP speaker to continue to forward data packets along known routes while the routing protocol information is being restored. |                                                                                                                                                  |
| networks  | list    | false    | -                     | nets         | Select the network to advertise, you have to set a Null route via System -> Routes                                                                                                                                        |                                                                                                                                                  |
| redistribute  | list    | false    | -                     | -         | Select other routing sources, which should be redistributed to the other nodes. Choose from: 'ospf', 'connected', 'kernel', 'rip', 'static'                                                                                                                             |                                                                                                                                                  |



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

    - name: Removing route 'test3'
      ansibleguy.opnsense.frr_bfd:
        ip: '10.0.0.1'
        state: 'absent'
```

### ansibleguy.opnsense.frr_bgp_general

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_bgp_general:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_bgp_general'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_bgp_general:
        as_number: 1337
        # id: '10.0.0.1'
        # graceful: false
        # networks: []
        # redistribute: []
        # enabled: true

    - name: Configuring general settings
      ansibleguy.opnsense.frr_bgp_general:
        as_number: 1337
        id: '10.0.0.1'
        graceful: true
        networks: ['10.0.10.0/24']
        redistribute: ['static']
        enabled: true

    - name: Disabling BGP
      ansibleguy.opnsense.frr_bgp_general:
        as_number: 1337
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_bgp_general'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data
```

