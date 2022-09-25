# OPNSense - Network interface module

**STATE**: unstable

**TESTS**: [vlan](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/interface_vlan.yml) | [vxlan](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/interface_vxlan.yml)

**API DOCS**: [Core - Interfaces](https://docs.opnsense.org/development/api/core/interfaces.html)

**BASE DOCS**: [VLAN](https://docs.opnsense.org/manual/other-interfaces.html?highlight=vlan#vlan) | [VxLAN](https://docs.opnsense.org/manual/other-interfaces.html?highlight=vlan#vxlan)

## Info

### ansibleguy.opnsense.interface_vlan

This module manages VLAN configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - VLAN'

### ansibleguy.opnsense.interface_vxlan

This module manages VXLAN configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - VXLAN'

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

### ansibleguy.opnsense.interface_vlan

| Parameter   | Type    | Required                              | Default value | Aliases               | Comment                                                                                                                                                            |
|:------------|:--------|:--------------------------------------|:--------------|:----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| description | string  | true                                  | -             | desc, name            | The unique description used to match the configured entries to the existing ones                                                                                   |
| interface | string  | false for state changes, else true    | -             | parent, port, int, if | The parent interface to add the vlan to. Existing VLAN capable interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port' |
| vlan | integer | false for state changes, else true    | -             | tag, id               | 802.1Q VLAN tag (between 1 and 4094)                                                                                                                               |
| priority | integer | false                                 | 0            | prio                  | 802.1Q VLAN PCP (between 0 and 7)                                                                                                                                  |
| reload         | boolean | false    | true          | -                     | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it manually after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md).         |

### ansibleguy.opnsense.interface_vxlan

| Parameter | Type    | Required                              | Default value | Aliases                                                      | Comment                                                                                                                                                                                                                                                                                |
|:----------|:--------|:--------------------------------------|:--------------|:-------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id        | integer | true                                  | -             | vxlanid, vni                                                 | The unique ID of the VxLAN                                                                                                                                                                                                                                                             |
| interface | string  | false for state changes, else true    | -             | vxlandev, device, int                                        | Optionally set an interface to bind the VxLAN to. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'                                                                                                                                 |
| local      | string | false for state changes, else true    | -             | source_address, source_ip, vxlanlocal, source, src           | Source IP for the VxLAN tunnel. The source address used in the encapsulating IPv4/IPv6 header. The address should already be assigned to an existing interface. When the interface is configured in unicast mode, the listening socket is bound to this address.                       |
| remote  | string  | false                                 | -             | remote_address, remote_ip, destination, vxlanremote, dest    | Remote IP for the VxLAN tunnel - if unicast is used. The interface can be configured in a unicast, or point-to-point, mode to create a tunnel between two hosts. This is the IP address of the remote end of the tunnel.                                                               |
| group  | string | false                                 | -             | multicast_group, multicast_address, multicast_ip, vxlangroup | Remote IP for the VxLAN tunnel - if multicast is used. The interface can be configured in a multicast mode to create a virtual network of hosts. This is the IP multicast group address the interface will join.                                                                                                                                                                                                                                |
| reload    | boolean | false    | true          | -                                                            | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it manually after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |



## Examples

### ansibleguy.opnsense.interface_vlan

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.interface_vlan:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'interface_vlan'

  tasks:
    - name: Example
      ansibleguy.opnsense.interface_vlan:
        description: 'example'
        interface: 'vtnet0'
        vlan: 100
        # priority: 0
        # debug: false
        # state: 'present'
        # reload: true

    - name: Adding VLAN
      ansibleguy.opnsense.interface_vlan:
        description: 'test1'
        interface: 'vtnet0'
        vlan: 100

    - name: Listing VLANs
      ansibleguy.opnsense.list:
      #  target: 'interface_vlan'
      register: existing_entries

    - name: Printing
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing VLAN
      ansibleguy.opnsense.interface_vlan:
        description: 'test1'
        state: 'absent'
```


### ansibleguy.opnsense.interface_vxlan

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.interface_vxlan:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'interface_vxlan'

  tasks:
    - name: Example
      ansibleguy.opnsense.interface_vxlan:
        id: 100
        local: '192.168.0.1'
        # remote: ''
        # group: ''
        # interface: 'lan'
        # debug: false
        # state: 'present'
        # reload: true

    - name: Adding VxLAN
      ansibleguy.opnsense.interface_vxlan:
        id: 100
        local: '192.168.0.1'
        interface: 'lan'

    - name: Listing VxLANs
      ansibleguy.opnsense.list:
      #  target: 'interface_vxlan'
      register: existing_entries

    - name: Printing
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing VxLAN
      ansibleguy.opnsense.interface_vxlan:
        id: 100
        state: 'absent'
```
