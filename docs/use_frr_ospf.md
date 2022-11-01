# OPNSense - FRR BGP modules

**STATE**: testing

**TESTS**: [frr_ospf_general](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_ospf_general.yml) | 


**API DOCS**: [Plugins - Quagga](https://docs.opnsense.org/development/api/plugins/quagga.html)

**BASE DOCS**: [Dynamic Routing](https://docs.opnsense.org/manual/dynamic_routing.html)

**FRR DOCS**: [FRRouting](https://docs.frrouting.org/) (_make sure you are looking at the current OPNSense package version!_)

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

### ansibleguy.opnsense.frr_ospf_general

| Parameter        | Type    | Required | Default value | Aliases                                             | Comment                                                                                                                                                                                                                                                        |
|:-----------------|:--------|:---------|:--------------|:----------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| carp             | boolean | false    | false         | carp_demote                                         | Register CARP status monitor, when no neighbors are found, consider this node less attractive. This feature needs syslog enabled using "Debugging" logging to catch all relevant status events. This option is not compatible with "Enable CARP Failover"      |
| id               | string  | false    | -             | router_id                                           | If you have a CARP setup, you may want to configure a router id in case of a conflict. (_4-byte field/IPv4 Address_)                                                                                                                                           |                                                                                                                                                  |
| cost             | integer | false    | -             | reference_cost, ref_cost                            | Here you can adjust the reference cost in Mbps for path calculation. Mostly needed when you bundle interfaces to higher bandwidth                                                                                                                              |                                                                                                                                                  |
| passive_ints     | list    | false    | -             | passive_interfaces                                  | Select the interfaces, where no OSPF packets should be sent to. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'                                                                                           |                                                                                                                                                  |
| redistribute     | list    | false    | -             | -                                                   | Select other routing sources, which should be redistributed to the other nodes. Choose from: 'bgp', 'connected', 'kernel', 'rip', 'static'                                                                                                                     |                                                                                                                                                  |
| redistribute_map | string  | false    | -             | -                                                   | Route Map to set for Redistribution                                                                                                                                                                                                                            |
| originate        | boolean | false    | false         | orig, advertise_default_gw                          | This will send the information that we have a default gateway                                                                                                                                                                                                  |
| originate_always | boolean | false    | false         | orig_always, always_advertise_default_gw            | This will send the information that we have a default gateway, regardless of if it is available                                                                                                                                                                |
| originate_metric | integer | false    | -             | orig_metric                                         | This let you manipulate the metric when advertising default gateway                                                                                                                                                                                            |
| reload           | boolean | false    | true                 | -       | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |
| enabled          | boolean | false    | true                 | -       | En- or disable the service                                                                                                                                                                                                                                     |

### ansibleguy.opnsense.frr_ospf_network

| Parameter           | Type    | Required                           | Default value | Aliases                                | Comment                                                                                                                                                                                                                                                                                                                                                               |
|:--------------------|:--------|:-----------------------------------|:--------------|:---------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| reload       | boolean | false    | true                 | -       | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

### ansibleguy.opnsense.frr_ospf_interface

| Parameter    | Type    | Required | Default value | Aliases | Comment                                                                                                                                                                                                                                                        |
|:-------------|:--------|:---------|:--------------|:--------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| reload       | boolean | false    | true          | -       | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

### ansibleguy.opnsense.frr_ospf_prefix_list

| Parameter | Type    | Required | Default value | Aliases    | Comment                                                                                                                                                                                                                                                        |
|:----------|:--------|:---------|:----------------------|:-----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name      | string | true    | -          | -          | The name of the prefix-list |
| seq       | string | false for state changes, else true    | -          | seq_number | The ACL sequence number (10-99) |
| network   | string | false for state changes, else true    | -          | net        | The network pattern you want to match. It's not validated so please be careful! |
| action    | string | false for state changes, else true    | -          | -          | Set permit for match or deny to negate the rule. One of: 'permit', 'deny' |
| reload    | boolean | false    | true          | -          | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

### ansibleguy.opnsense.frr_ospf_route_map

| Parameter      | Type    | Required | Default value | Aliases  | Comment                                                                                                                                                                                                                                                        |
|:-------------|:--------|:---------|:----------------------|:----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| reload         | boolean | false    | true          | -        | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

### ansibleguy.opnsense.frr_ospf3_general

| Parameter    | Type    | Required | Default value | Aliases                                             | Comment                                                                                                                                                                                                                                                   |
|:-------------|:--------|:---------|:--------------|:----------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| carp  | boolean | false    | false         | carp_demote                                         | Register CARP status monitor, when no neighbors are found, consider this node less attractive. This feature needs syslog enabled using "Debugging" logging to catch all relevant status events. This option is not compatible with "Enable CARP Failover" |
| id  | string  | false    | -             | router_id                                           | If you have a CARP setup, you may want to configure a router id in case of a conflict. (_4-byte field/IPv4 Address_)                                                                                                                                      |                                                                                                                                                  |
| redistribute  | list    | false    | -             | -                                                   | Select other routing sources, which should be redistributed to the other nodes. Choose from: 'bgp', 'connected', 'kernel', 'rip', 'static'                                                                                                                |                                                                                                                                                  |
| reload       | boolean | false    | true                 | -       | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |
| enabled          | boolean | false    | true                 | -       | En- or disable the service                                                                                                                                                                                                                                     |

### ansibleguy.opnsense.frr_ospf3_interface

| Parameter    | Type    | Required | Default value         | Aliases   | Comment                                                                                                                                                                                                                                                                                                                                                                |
|:-------------|:--------|:---------|:----------------------|:----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields     | string | false    | ['interface', 'area'] | -                                      | Fields that are used to match configured interface with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'interface', 'area', 'passive', 'carp_depend_on', 'network_type' |
| interface       | string  | true     | -                     | name, int | Interface to configure. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'                                                                                                                                                                                                                                           |
| area       | string  | false for state changes, else true    | -                     | -         | Area in wildcard mask style like 0.0.0.0 and no decimal 0                                                                                                                                                                                                                                                                                                              |
| passive       | boolean | false    | false                 | -         |                                                                                                                                                                                                                                                                                                                                                                        |
| cost       | integer | false    | -                     | -         |                                                                                                                                                                                                                                                                                                                                                                        |
| cost_demoted       | integer  | false    | -                     | -         |                                                                                                                                                                                                                                                                                                                                                                        |
| carp_depend_on       | string  | false    | -                     | -         | The carp VHID to depend on, when this virtual address is not in master state, the interface cost will be set to the demoted cost. Integer between 1 and 65535                                                                                                                                                                                                          |
| hello_interval       | integer  | false    | -                     | hello     | Integer between 0 and 4294967295                                                                                                                                                                                                                                                                                                                                       |
| dead_interval       | integer  | false    | -                     | dead     | Integer between 0 and 4294967295                                                                                                                                                                                                                                                                                                                                       |
| retransmit_interval       | integer  | false    | -                     | retransmit     | Integer between 0 and 4294967295                                                                                                                                                                                                                                                                                                                                       |
| transmit_delay       | integer  | false    | -                     | delay     | Integer between 0 and 4294967295                                                                                                                                                                                                                                                                                                                                       |
| priority       | integer  | false    | -                     | prio     | Integer between 0 and 4294967295                                                                                                                                                                                                                                                                                                                                       |
| network_type       | string  | false    | -                     | nw_type         | One of: 'broadcast', 'point-to-point'                                                                                                                                                                                                                                                                                                                                  |
| reload       | boolean | false    | true                  | -         | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md).                                                                                                         |

## Examples

### ansibleguy.opnsense.frr_ospf_general

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_ospf_general:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_ospf_general'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_ospf_general:
        # id: '10.0.0.1'
        # cost: 200
        # passive_ints: []
        # redistribute: []
        # redistribute_map: ''
        # carp: false
        # originate: false
        # originate_always: false
        # originate_metric: 1000
        # enabled: true

    - name: Configuring general settings
      ansibleguy.opnsense.frr_ospf_general:
        id: '10.0.1.1'
        cost: 300
        passive_ints: ['lan']
        redistribute: ['static', 'bgp']
        originate: true
        originate_metric: 1000

    - name: Disabling OSPF
      ansibleguy.opnsense.frr_ospf_general:
        id: '10.0.1.1'
        cost: 300
        passive_ints: ['lan']
        redistribute: ['static', 'bgp']
        originate: true
        originate_metric: 1000
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_ospf_general'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data
```

### ansibleguy.opnsense.frr_ospf3_general

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_ospf3_general:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_ospf3_general'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_ospf3_general:
        # id: '10.0.0.1'
        # redistribute: []
        # carp: false
        # enabled: true

    - name: Configuring general settings
      ansibleguy.opnsense.frr_ospf3_general:
        id: '10.0.1.1'
        redistribute: ['static']

    - name: Disabling OSPFv3
      ansibleguy.opnsense.frr_ospf3_general:
        id: '10.0.1.1'
        redistribute: ['static']
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_ospf3_general'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data
```

### ansibleguy.opnsense.frr_ospf3_interface

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_ospf3_interface:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      match_fields: ['interface']

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_ospf3_interface'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_ospf3_interface:
        interface: 'opt1'
        # area: '0.0.0.0'
        # cost: 10
        # cost_demoted: 10
        # hello_interval: 10
        # dead_interval: 10
        # retransmit_interval: 10
        # transmit_delay: 10
        # priority: 10
        # network_type: ''
        # carp_depend_on: ''
        # passive: false
        # enabled: true
        # match_fields: ['interface', 'area']

    - name: Configuring interface
      ansibleguy.opnsense.frr_ospf3_interface:
        interface: 'opt1'
        area: '0.0.0.0'
        cost: 500
        cost_demoted: 2000
        hello_interval: 60
        dead_interval: 30
        retransmit_interval: 60
        transmit_delay: 60
        priority: 30
        network_type: 'point-to-point'

    - name: Disabling interface
      ansibleguy.opnsense.frr_ospf3_interface:
        interface: 'opt1'
        area: '0.0.0.0'
        cost: 500
        cost_demoted: 2000
        hello_interval: 60
        dead_interval: 30
        retransmit_interval: 60
        transmit_delay: 60
        priority: 30
        network_type: 'point-to-point'
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_ospf3_interface'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing interface
      ansibleguy.opnsense.frr_ospf3_interface:
        interface: 'opt1'
        state: 'absent'
```
