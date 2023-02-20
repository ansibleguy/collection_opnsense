# WireGuard

**STATE**: unstable

**TESTS**: [wireguard_server](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/wireguard_server.yml) | 
[wireguard_peer](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/wireguard_peer.yml) | 
[wireguard_general](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/wireguard_general.yml) | 
[wireguard_show](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/wireguard_show.yml) 

**API Docs**: [Plugin - Wireguard](https://docs.opnsense.org/development/api/plugins/wireguard.html)

**Service Docs**: [WireGuard - Site to Site](https://docs.opnsense.org/manual/how-tos/wireguard-s2s.html) | [WireGuard - Client to Site](https://docs.opnsense.org/manual/how-tos/wireguard-client.html)

## Prerequisites

You need to install the WireGuard plugin:
```
os-wireguard
```

You can also install it using the [package module](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/use_package.md).

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/use_basic.md#definition)

### ansibleguy.opnsense.wireguard_server

| Parameter      | Type    | Required | Default value | Aliases                                                                                            | Comment                                                                                                                                                                                                                                                                                        |
|:---------------|:--------|:---------|:--------------|:---------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name           | string  | true     | -             | -                                                                                                  | The unique name of the local WireGuard server instance                                                                                                                                                                                                                                         |
| peers          | list  | false     | -             | clients                                                                                            | List of existing peers that                                                                                                                                                                                                                                                                    |
| allowed_ips    | list    | false    | -             | tunnel_ips, tunnel_ip, tunneladdress, tunnel_adresses, tunnel_address, addresses, address, allowed | One or multiple IP addresses that are used inside the tunnel                                                                                                                                                                                                                                   |
| public_key     | string  | false    | -             | pubkey, pub                                                                                        | Optionally provide an existing WireGuard Public Key. If none is provided - a key-pair will be generated automatically or the existing one will be used.                                                                                                                                        |
| private_key    | string  | false    | -             | privkey, priv                                                                                      | Optionally provide an existing WireGuard Private Key. If none is provided - a key-pair will be generated automatically or the existing one will be used.                                                                                                                                       |
| port           | integer | false    | -             | -                                                                                                  | Optionally provide a port for the server instance. Needed if dynamic peers will connect to this instance!                                                                                                                                                                                      |
| mtu            | integer | false    | 1420          | -                                                                                                  | Integer between 1 and 9300                                                                                                                                                                                                                                                                     |
| dns_servers    | list    | false    | -             | dns                                                                                                | List of DNS servers that will be used to resolve peer endpoint-names                                                                                                                                                                                                                           |
| disable_routes | boolean | false    | false         | disableroutes                                                                                      | If automatically created routes should be disabled. Needs to be set if you want to use [policy-based routing](https://docs.opnsense.org/manual/firewall.html#policy-based-routing), [dynamic routing](https://docs.opnsense.org/manual/dynamic_routing.html) or 'manually' created static routes |
| gateway        | string  | false    | -             | gw                                                                                                 | IP address to use as gateway. Can only be used if you enable the 'disable_routes' option.                                                                                                                                                                                                      |
| reload         | boolean | false    | true          | -                                                                                                  | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/use_reload.md).         |

### ansibleguy.opnsense.wireguard_peer

| Parameter   | Type    | Required | Default value | Aliases                                                                                            | Comment                                                                                                                                                                                                                                                                                |
|:------------|:--------|:---------|:--------------|:---------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name        | string  | true     | -             | -                                                                                                  | The unique name of the local WireGuard peer                                                                                                                                                                                                                                            |
| endpoint      | string    | false    | -             | server_address, serveraddress, target, server                                                      | Peer endpoint IP address or DNS-hostname                                                                                                                                                                                                                                               |
| allowed_ips | list    | false for state changes, else true    | -             | tunnel_ips, tunnel_ip, tunneladdress, tunnel_adresses, tunnel_address, addresses, address, allowed | One or multiple IP addresses used by the peer inside the tunnel                                                                                                                                                                                                                        |
| public_key  | string  | false for state changes, else true    | -             | pubkey, pub                                                                                        | Provide the WireGuard Public Key of the peer. Used to identify the peer                                                                                                                                                                                                                |
| psk         | string  | false    | -             | -                                                                                                  | Optionally provide an PSK. The pre-shared key (PSK) is an optional security improvement as per the WireGuard protocol and should be a unique PSK per client for highest security.                                                                                                      |
| port        | integer | false    | -             | -                                                                                                  | Optionally provide the port of the peer instance                                                                                                                                                                                                                                       |
| keepalive   | integer | false    | -             | -                                                                                                  | Integer between 1 and 86400. Should be used if one of the connection-members is behind NAT                                                                                                                                                                                             |
| reload      | boolean | false    | true          | -                                                                                                  | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/use_reload.md). |

### ansibleguy.opnsense.wireguard_show

| Parameter   | Type    | Required | Default value | Aliases                                                                                            | Comment                                                 |
|:------------|:--------|:---------|:--------------|:---------------------------------------------------------------------------------------------------|:--------------------------------------------------------|
| target      | string  | false    | handshake     | -                                                                                                  | What information to query. One of: 'handshake', 'config' |

### ansibleguy.opnsense.wireguard_general

| Parameter | Type    | Required | Default value | Aliases                                                                                            | Comment                                         |
|:----------|:--------|:---------|:--------------|:---------------------------------------------------------------------------------------------------|:------------------------------------------------|
| enabled   | boolean | false    | true          | -                                                                                                  | Used to enable or disable the wireguard service |


## Usage

To make a dynamic WireGuard endpoint to re-connect you may want to create a [gateway monitoring (_dpinger_)](https://docs.opnsense.org/manual/gateways.html#settings) targeting the remote tunnel-address.


## Examples

### ansibleguy.opnsense.wireguard_general

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.wireguard_general:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.wireguard_general:
        # enabled: true

    - name: Enabling WireGuard service
      ansibleguy.opnsense.wireguard_general:
        enabled: true
```

### ansibleguy.opnsense.wireguard_show

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.wireguard_show:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.wireguard_show:
        # target: 'handshake'

    - name: Querying the current WireGuard handshakes
      ansibleguy.opnsense.wireguard_show:
        target: 'handshake'
      register: wg_hands

    - name: Printing
      ansible.builtin.debug:
        var: wg_hands.data
```

### ansibleguy.opnsense.wireguard_peer

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.wireguard_peer:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'wireguard_peer'

  tasks:
    - name: Example
      ansibleguy.opnsense.wireguard_peer:
        name: 'example'
        # allowed_ips: []
        # enpoint: ''
        # port: ''
        # public_key: ''
        # psk: ''
        # keepalive: ''
        # enabled: true
        # debug: false
        # state: 'present'
        # reload: true

    - name: Adding peer
      ansibleguy.opnsense.wireguard_peer:
        name: 'test1'
        endpoint: 'wg.template.ansibleguy.net'
        allowed_ips: ['10.200.0.1/32']
        public_key: 'gTuhGXA28/qRSLPnH3szr2+A4l3C4tKlUsOORV63+SE='

    - name: Disabling peer
      ansibleguy.opnsense.wireguard_peer:
        name: 'test1'
        enabled: false

    - name: Listing peers
      ansibleguy.opnsense.list:
      #  target: 'wireguard_peer'
      register: existing_entries

    - name: Printing
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing peer
      ansibleguy.opnsense.wireguard_peer:
        name: 'test1'
        state: 'absent'
```

### ansibleguy.opnsense.wireguard_server

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.wireguard_server:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'wireguard_server'

  tasks:
    - name: Example
      ansibleguy.opnsense.wireguard_server:
        name: 'example'
        # allowed_ips: []
        # peers: []
        # port: ''
        # public_key: ''
        # private_key: ''
        # mtu: 1420
        # dns_servers: []
        # disable_routes: false
        # gateway: ''
        # enabled: true
        # debug: false
        # state: 'present'
        # reload: true

    - name: Adding server
      ansibleguy.opnsense.wireguard_server:
        name: 'test1'
        allowed_ips: ['10.200.0.1/32']
        peers: ['peer1']
        port: 51820

    - name: Disabling server
      ansibleguy.opnsense.wireguard_server:
        name: 'test1'
        enabled: false

    - name: Listing servers
      ansibleguy.opnsense.list:
      #  target: 'wireguard_server'
      register: existing_entries

    - name: Printing
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing server
      ansibleguy.opnsense.wireguard_server:
        name: 'test1'
        state: 'absent'
```
