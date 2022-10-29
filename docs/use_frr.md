# OPNSense - FRR module

**STATE**: testing

**TESTS**: [frr_bfd](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_bfd.yml) | [frr_bgp_general](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_bgp_general.yml) | [frr_bgp_neighbor](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/frr_bgp_neighbor.yml)

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

### ansibleguy.opnsense.frr_bgp_general

| Parameter    | Type    | Required | Default value         | Aliases   | Comment                                                                                                                                                                                                                                                        |
|:-------------|:--------|:---------|:----------------------|:----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| as_number           | string  | true     | -                     | as, as_nr | BGP AS-Number                                                                                                                                                                                                                                                  |
| id  | string  | false    | -                     | router_id | In some cases it might be clearer to set a fixed router-id. (_4-byte field/IPv4 Address_)                                                                                                                                                                      |                                                                                                                                                  |
| graceful  | boolean | false    | -                     | -         | BGP graceful restart functionality as defined in RFC-4724 defines the mechanisms that allows BGP speaker to continue to forward data packets along known routes while the routing protocol information is being restored.                                      |                                                                                                                                                  |
| networks  | list    | false    | -                     | nets         | Select the network to advertise, you have to set a Null route via System -> Routes                                                                                                                                                                             |                                                                                                                                                  |
| redistribute  | list    | false    | -                     | -         | Select other routing sources, which should be redistributed to the other nodes. Choose from: 'ospf', 'connected', 'kernel', 'rip', 'static'                                                                                                                    |                                                                                                                                                  |
| reload       | boolean | false    | true                 | -       | If the running config should be reloaded on change - this will take some time. You might want to reload it manually after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

### ansibleguy.opnsense.frr_bgp_neighbor

| Parameter           | Type    | Required                           | Default value | Aliases                                | Comment                                                                                                                                                                                                                                                                                                                                                               |
|:--------------------|:--------|:-----------------------------------|:--------------|:---------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields     | string | false    | ['ip', 'description']              | -                                      | Fields that are used to match configured neighbor with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'ip', 'as_number', 'weight', 'local_ip', 'source_int', 'ipv6_link_local_int', 'disable_connected_check', 'description', 'prefix_list_in', 'prefix_list_out', 'route_map_in', 'route_map_out' |
| as_number           | string  | false for state changes, else true | -             | as, as_nr, remote_as                   | BGP AS-Number of the neighbor                                                                                                                                                                                                                                                                                                                                         |
| ip                  | string  | false for state changes, else true | -             | peer, peer_ip, address, neighbor       | IP-address of the neighbor                                                                                                                                                                                                                                                                                                                                            |
| password            | string  | false                              | -             | pwd                                    | Set a (MD5-hashed) password for BGP authentication                                                                                                                                                                                                                                                                                                                    |
| weight              | integer | false                              | -             | -                                      | Specify a default weight value for the neighbor’s routes. Integer between 0 and 65535                                                                                                                                                                                                                                                                                 |
| local_ip            | string  | false                              | -             | local                                  | Set the local IP connecting to the neighbor. This is only required for BGP authentication.                                                                                                                                                                                                                                                                            |
| source_int          | string  | false                              | -             | src_int, update_src, update_source     | Physical name of the IPv4 interface facing the peer. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'                                                                                                                                                                                                             |
| ipv6_link_local_int | string  | false                              | -             | v6_ll_int, ipv6_ll_int, link_local_int | Interface to use for IPv6 link-local neighbours. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'                                                                                                                                                                                                                                                                                                                     |
| next_hop_self                    | boolean | false                              | false         | nhs                                    |                                                                                                                                                                                                                                                                                                                                                                       |
| next_hop_self_all                    | boolean | false                              | false         | nhsa                                   | Add the parameter "all" after next-hop-self command                                                                                                                                                                                                                                                                                                                   |
| multi_hop                    | boolean | false                              | false         | -                                      | Specifying ebgp-multihop allows sessions with eBGP neighbors to establish when they are multiple hops away. When the neighbor is not directly connected and this knob is not enabled, the session will not establish.                                                                                                                                                 |
| multi_protocol                    | boolean | false                              | false         | -                                      | Is this neighbour multiprotocol capable per RFC 2283                                                                                                                                                                                                                                                                                                                  |
| rrclient                    | boolean | false                              | false         | route_reflector_client                 |                                                                                                                                                                                                                                                                                                                                                                       |
| bfd                    | boolean | false                              | false         | -                                      | Enable BFD support for this neighbor                                                                                                                                                                                                                                                                                                                                  |
| send_default_route                    | boolean | false                              | false         | default_originate                      |                                                                                                                                                                                                                                                                                                                                                                       |
| as_override                    | boolean | false                              | false         | asoverride                             | Override AS number of the originating router with the local AS number. This command is only allowed for eBGP peers                                                                                                                                                                                                                                                    |
| disable_connected_check                    | boolean | false                              | false         | asoverride                             | Allow peerings between directly connected eBGP peers using loopback addresses                                                                                                                                                                                                                                                                                         |
| keepalive                    | integer | false                              | 60            | keep_alive                             | Keepalive timer to check if the neighbor is still up. Integer between 1 and 1000                                                                                                                                                                                                                                                                                      |
| hold_down                    | integer | false                              | 180           | holddown                               | The time in seconds when a neighbor is considered dead. This is usually 3 times the keepalive timer. Integer between 3 and 3000                                                                                                                                                                                                                                       |
| connect_timer                    | integer | false                              | -             | connecttimer                           | The time in seconds how fast a neighbor tries to reconnect. Integer between 1 and 65000                                                                                                                                                                                                                                                                               |
| description  | string          | false    | -                     | desc                                   | Optional description for the neighbor                                                                                                                                                                                                                                                                                                                                 |
| prefix_list_in                    | string  | false                              | -             | prefix_in, pre_in                      | Prefix-List for inbound direction                                                                                                                                                                                                                                                                                                                                     |
| prefix_list_out                    | string  | false                              | -             | prefix_out, pre_out                    | Prefix-List for outbound direction                                                                                                                                                                                                                                                                                                                                    |
| route_map_in                    | string  | false                              | -             | map_in, rm_in                          | Route-Map for inbound direction                                                                                                                                                                                                                                                                                                                                       |
| route_map_out                    | string  | false                              | -             | map_out, rm_out                        | Route-Map for outbound direction                                                                                                                                                                                                                                                                                                                                      |


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

    - name: Removing neighbor 'test3'
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

    - name: Disabling BGP
      ansibleguy.opnsense.frr_bgp_general:
        as_number: 1337
        id: '10.0.0.1'
        graceful: true
        networks: ['10.0.10.0/24']
        redistribute: ['static']
        enabled: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'frr_bgp_general'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data
```

### ansibleguy.opnsense.frr_bgp_neighbor

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.frr_bgp_neighbor:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      match_fields: ['ip']

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'frr_bgp_neighbor'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_bgp_neighbor:
        as_number: 1337
        ip: '10.0.0.1'
        # password: "{{ 'random' | hash('md5') }}"
        # weight: 200
        # local_ip: '10.0.0.254'
        # source_int: 'opt1'
        # ipv6_link_local_int: 'opt1'
        # next_hop_self: false
        # next_hop_self_all: false
        # multi_hop: false
        # multi_protocol: false
        # rrclient: false
        # bfd: false
        # send_default_route: false
        # as_override: false
        # disable_connected_check: false
        # keepalive: 60
        # hold_down: 180
        # connect_timer: 30
        # description: 'test1'
        # prefix_list_in: 'prefix1'
        # prefix_list_out: 'prefix2'
        # route_map_in: 'map1'
        # route_map_out: 'map2'
        # enabled: true

    - name: Creating neighbor
      ansibleguy.opnsense.frr_bgp_neighbor:
        description: 'test2'
        as_number: 1337
        ip: '10.0.0.1'
        password: "{{ 'random' | hash('md5') }}"
        weight: 200
        source_int: 'opt1'
        multi_protocol: true
        keepalive: 45
        hold_down: 135

    - name: Disabling neighbor
      ansibleguy.opnsense.frr_bgp_neighbor:
        description: 'test2'
        as_number: 1337
        ip: '10.0.0.1'
        password: "{{ 'random' | hash('md5') }}"
        weight: 200
        source_int: 'opt1'
        multi_protocol: true
        keepalive: 45
        hold_down: 135
        enabled: false

    - name: Pulling neighbors
      ansibleguy.opnsense.list:
      #  target: 'frr_bgp_neighbor'
      register: existing_entries

    - name: Printing neighbors
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing neighbor
      ansibleguy.opnsense.frr_bgp_neighbor:
        ip: '10.0.0.1'
        state: 'absent'
```

