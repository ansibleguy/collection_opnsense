# FRR OSPF

**STATE**: unstable

**TESTS**: [frr_ospf_general](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_ospf_general.yml) |
[frr_ospf_prefix_list](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_ospf_prefix_list.yml) |
[frr_ospf_interface](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_ospf_interface.yml) |
[frr_ospf_route_map](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_ospf_route_map.yml) |
[frr_ospf_network](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_ospf_network.yml) |
[frr_ospf3_general](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_ospf3_general.yml) |
[frr_ospf3_interface](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_ospf3_interface.yml)


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

### OSPF

#### ansibleguy.opnsense.frr_ospf_general

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

#### ansibleguy.opnsense.frr_ospf_network

| Parameter    | Type    | Required                           | Default value  | Aliases                              | Comment                                                                                                                                                                                                                                                          |
|:-------------|:--------|:-----------------------------------|:---------------|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields | string | false                              | ['ip', 'mask'] | -                                    | Fields that are used to match configured interface with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'ip', 'mask', 'area', 'area_range'                                                     |
| ip           | string  | true                               | -              | network_address, nw_address, address |                                                                                                                                                                                                                                                                  |
| mask         | string  | true                               | -              | network_mask, nw_mask                | Integer between 0 and 32                                                                                                                                                                                                                                         |
| area         | string  | false for state changes, else true | -              | -                                    | Area in wildcard mask style like 0.0.0.0 and no decimal 0. Only use Area in Interface tab or in Network tab once                                                                                                                                                 |
| area_range   | string  | -                                  | -              | -                                    | Here you can summarize a network for this area like 192.168.0.0/23                                                                                                                                                 |
| prefix_list_in   | string  | -                                  | -              | prefix_in, pre_in                    | Prefix-List for inbound direction                                                                                                                                                 |
| prefix_list_out   | string  | -                                  | -              | prefix_out, pre_out                  | Prefix-List for outbound direction                                                                                                                                                 |
| reload       | boolean | false                              | true           | -                                    | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

#### ansibleguy.opnsense.frr_ospf_interface

| Parameter           | Type    | Required                               | Default value         | Aliases   | Comment                                                                                                                                                                                                                                                          |
|:--------------------|:--------|:---------------------------------------|:----------------------|:----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields        | string | false                                  | ['interface', 'area'] | -                                      | Fields that are used to match configured interface with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'interface', 'area', 'passive', 'carp_depend_on', 'network_type'                       |
| interface           | string  | true                                   | -                     | name, int | Interface to configure. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'                                                                                                                                     |
| area                | string  | false for state changes, else true     | -                     | -         | Area in wildcard mask style like 0.0.0.0 and no decimal 0                                                                                                                                                                                                        |
| auth_type           | string  | false                                  | -                     | -         | What authentication type to use. Currently only 'message-digest' is supported                                                                                                                                                                                    |
| auth_key            | string  | true if 'auth_type' is set, else false                                  | -                     | -         | The key to authenticate                                                                                                                                                                                                                                          |
| auth_key_id         | integer | false | 1                     | -         | Integer between 1 and 255                                                                                                                                                                                                                                        |
| cost                | integer | false                                  | -                     | -         | Integer between 1 and 65535                                                                                                                                                                                                                                                                 |
| cost_demoted        | integer  | false                                  | 65535                     | -         | Integer between 1 and 65535                                                                                                                                                                                                                                           |
| carp_depend_on      | string  | false                                  | -                     | -         | The carp VHID to depend on, when this virtual address is not in master state, the interface cost will be set to the demoted cost. Integer between 1 and 65535                                                                                                    |
| hello_interval      | integer  | false                                  | -                     | hello     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| dead_interval       | integer  | false                                  | -                     | dead     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| retransmit_interval | integer  | false                                  | -                     | retransmit     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| transmit_delay      | integer  | false                                  | -                     | delay     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| priority            | integer  | false                                  | -                     | prio     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| network_type        | string  | false                                  | -                     | nw_type         | One of: 'broadcast', 'non-broadcast', 'point-to-multipoint', 'point-to-point'                                                                                                                                                                                    |
| reload              | boolean | false                                  | true                  | -         | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

#### ansibleguy.opnsense.frr_ospf_prefix_list

| Parameter | Type    | Required | Default value | Aliases    | Comment                                                                                                                                                                                                                                                        |
|:----------|:--------|:---------|:----------------------|:-----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name      | string | true    | -          | -          | The name of the prefix-list |
| seq       | string | false for state changes, else true    | -          | seq_number | The ACL sequence number (10-99) |
| network   | string | false for state changes, else true    | -          | net        | The network pattern you want to match. It's not validated so please be careful! |
| action    | string | false for state changes, else true    | -          | -          | Set permit for match or deny to negate the rule. One of: 'permit', 'deny' |
| reload    | boolean | false    | true          | -          | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

#### ansibleguy.opnsense.frr_ospf_route_map

| Parameter    | Type    | Required | Default value | Aliases   | Comment                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:-------------|:--------|:---------|:--------------|:----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name           | string  | true     | -             | -         | Name to identify the route-map by                                                                                                                                                                                                                                                                                                                                                                                                  |
| id  | integer | false for state changes, else true    | -             | -         | Route-map ID between 10 and 99. Be aware that the sorting will be done under the hood, so when you add an entry between it get's to the right position                                                                                                                                                                                                                                                                             |                                                                                                                                                  |
| action  | string  | false for state changes, else true    | -             | -         | Set permit for match or deny to negate the rule. One of: 'permit', 'deny'                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                  |
| prefix_list  | list    | false    | -             | prefix    | List of prefix-list entries to link                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                  |
| set  | string  | false    | -             | -         | Free text field for your set, please be careful! You can set e.g. "local-preference 300" or "community 1:1" (http://www.nongnu.org/quagga/docs/docs-multi/Route-Map-Set-Command.html#Route-Map-Set-Command)                                                                                                                                                                                                                        |                                                                                                                                                  |
| reload       | boolean | false    | true          | -         | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md).                                                                                                                                                                   |

----

### OSPFv3 (_IPv6_)

#### ansibleguy.opnsense.frr_ospf3_general

| Parameter    | Type    | Required | Default value | Aliases                                             | Comment                                                                                                                                                                                                                                                   |
|:-------------|:--------|:---------|:--------------|:----------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| carp  | boolean | false    | false         | carp_demote                                         | Register CARP status monitor, when no neighbors are found, consider this node less attractive. This feature needs syslog enabled using "Debugging" logging to catch all relevant status events. This option is not compatible with "Enable CARP Failover" |
| id  | string  | false    | -             | router_id                                           | If you have a CARP setup, you may want to configure a router id in case of a conflict. (_4-byte field/IPv4 Address_)                                                                                                                                      |                                                                                                                                                  |
| redistribute  | list    | false    | -             | -                                                   | Select other routing sources, which should be redistributed to the other nodes. Choose from: 'bgp', 'connected', 'kernel', 'rip', 'static'                                                                                                                |                                                                                                                                                  |
| reload       | boolean | false    | true                 | -       | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |
| enabled          | boolean | false    | true                 | -       | En- or disable the service                                                                                                                                                                                                                                     |

#### ansibleguy.opnsense.frr_ospf3_interface

| Parameter    | Type    | Required | Default value         | Aliases   | Comment                                                                                                                                                                                                                                                          |
|:-------------|:--------|:---------|:----------------------|:----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields     | string | false    | ['interface', 'area'] | -                                      | Fields that are used to match configured interface with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'interface', 'area', 'passive', 'carp_depend_on', 'network_type'                       |
| interface       | string  | true     | -                     | name, int | Interface to configure. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'                                                                                                                                     |
| area       | string  | false for state changes, else true    | -                     | -         | Area in wildcard mask style like 0.0.0.0 and no decimal 0                                                                                                                                                                                                        |
| passive       | boolean | false    | false                 | -         |                                                                                                                                                                                                                                                                  |
| cost       | integer | false    | -                     | -         | Integer between 0 and 4294967295                                                                                                                                                                                                                                      |
| cost_demoted       | integer  | false    | -                     | 65535         | Integer between 1 and 65535                                                                                                                                                                                                                                      |
| carp_depend_on       | string  | false    | -                     | -         | The carp VHID to depend on, when this virtual address is not in master state, the interface cost will be set to the demoted cost. Integer between 1 and 65535                                                                                                    |
| hello_interval       | integer  | false    | -                     | hello     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| dead_interval       | integer  | false    | -                     | dead     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| retransmit_interval       | integer  | false    | -                     | retransmit     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| transmit_delay       | integer  | false    | -                     | delay     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| priority       | integer  | false    | -                     | prio     | Integer between 0 and 4294967295                                                                                                                                                                                                                                 |
| network_type       | string  | false    | -                     | nw_type         | One of: 'broadcast', 'point-to-point'                                                                                                                                                                                                                            |
| reload       | boolean | false    | true                  | -         | If the running config should be reloaded on change - this will take some time. You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

## Examples

### OSPF (_IPv4_)

#### ansibleguy.opnsense.frr_ospf_general

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

#### ansibleguy.opnsense.frr_ospf_prefix_list

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_ospf_prefix_list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_ospf_prefix_list'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_ospf_prefix_list:
        name: 'example'
        seq: 10
        action: 'permit'
        network: '10.0.0.0/24'
        # enabled: true

    - name: Configuring prefix-list
      ansibleguy.opnsense.frr_ospf_prefix_list:
        name: 'test2'
        seq: 25
        action: 'permit'
        network: '10.0.1.0/24'

    - name: Disabling prefix-list
      ansibleguy.opnsense.frr_ospf_prefix_list:
        name: 'test2'
        seq: 25
        action: 'permit'
        network: '10.0.1.0/24'
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_ospf_prefix_list'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing prefix-list
      ansibleguy.opnsense.frr_ospf_prefix_list:
        name: 'test2'
        state: 'absent'
```

#### ansibleguy.opnsense.frr_ospf_route_map

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_ospf_route_map:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_ospf_route_map'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_ospf_route_map:
        name: 'example'
        id: 10
        action: 'permit'
        # prefix_list: []
        # set: ''
        # enabled: true

    - name: Configuring route-map
      ansibleguy.opnsense.frr_ospf_route_map:
        name: 'test2'
        id: 65
        action: 'permit'
        set: 'local-preference 300'

    - name: Disabling route-map
      ansibleguy.opnsense.frr_ospf_route_map:
        name: 'test2'
        id: 65
        action: 'permit'
        set: 'local-preference 300'
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_ospf_route_map'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing route-map
      ansibleguy.opnsense.frr_ospf_route_map:
        name: 'test2'
        state: 'absent'
```

#### ansibleguy.opnsense.frr_ospf_network

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_ospf_network:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      match_fields: ['ip', 'mask']

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_ospf_route_map'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_ospf_network:
        ip: '10.0.0.0'
        mask: 24
        area: '0.0.0.0'
        # area_range: ''
        # enabled: true

    - name: Configuring network
      ansibleguy.opnsense.frr_ospf_network:
        ip: '10.0.1.0'
        mask: 28
        area: '0.0.1.0'

    - name: Disabling network
      ansibleguy.opnsense.frr_ospf_network:
        ip: '10.0.1.0'
        mask: 28
        area: '0.0.1.0'
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_ospf_network'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing network
      ansibleguy.opnsense.frr_ospf_network:
        ip: '10.0.1.0'
        mask: 28
        state: 'absent'
```

#### ansibleguy.opnsense.frr_ospf_interface

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_ospf_interface:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      match_fields: ['interface']

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_ospf_interface'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_ospf_interface:
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
        # auth_type: ''
        # auth_key: ''
        # auth_key_id: 1
        # enabled: true
        # match_fields: ['interface', 'area']

    - name: Configuring interface
      ansibleguy.opnsense.frr_ospf_interface:
        interface: 'opt1'
        area: '0.0.0.0'
        cost: 500
        cost_demoted: 2000
        hello_interval: 60
        dead_interval: 30
        retransmit_interval: 60
        transmit_delay: 60
        priority: 30
        network_type: 'point-to-multipoint'
        auth_type: 'message-digest'
        auth_key: "{{ 'random' | hash('md5') }}"

    - name: Disabling interface
      ansibleguy.opnsense.frr_ospf_interface:
        interface: 'opt1'
        area: '0.0.0.0'
        cost: 500
        cost_demoted: 2000
        hello_interval: 60
        dead_interval: 30
        retransmit_interval: 60
        transmit_delay: 60
        priority: 30
        network_type: 'point-to-multipoint'
        auth_type: 'message-digest'
        auth_key: "{{ 'random' | hash('md5') }}"
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_ospf_interface'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing interface
      ansibleguy.opnsense.frr_ospf_interface:
        interface: 'opt1'
        state: 'absent'
```

----

### OSPFv3 (_IPv6_)

#### ansibleguy.opnsense.frr_ospf3_general

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

#### ansibleguy.opnsense.frr_ospf3_interface

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
