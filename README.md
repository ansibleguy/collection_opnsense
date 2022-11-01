# Ansible Collection - ansibleguy.opnsense

[![Functional Test Status](https://badges.ansibleguy.net/opnsense.collection.test.svg)](https://github.com/ansibleguy/collection_opnsense/blob/stable/scripts/test.sh)
[![Lint Test Status](https://badges.ansibleguy.net/opnsense.collection.lint.svg)](https://github.com/ansibleguy/collection_opnsense/blob/stable/scripts/lint.sh)

---

## Contribute

Feel free to contribute to this project using [pull-requests](https://github.com/ansibleguy/collection_opnsense/pulls), [issues](https://github.com/ansibleguy/collection_opnsense/issues) and [discussions](https://github.com/ansibleguy/collection_opnsense/discussions)!

**What to contribute**:

* add ansible-based [tests](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests) for some error-case(s) you have encountered
* extend or correct the [documentation](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs)
* contribute code fixes or optimizations
* implement additional API endpoints => see [development guide](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/develop.md)
* test unstable modules and report bugs/errors

---

## Requirements

The [httpx python module](https://www.python-httpx.org/) is used for API communications!

```bash
python3 -m pip install httpx
```

The [validators python module](https://validators.readthedocs.io/) is used to validate user-provided data on the client-side.

```bash
python3 -m pip install validators
```

Then - install the collection itself:

```bash
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git

# or for easier development

cd $PLAYBOOK_DIR
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git -p ./collections
```

---

## Modules

**Development States**:

not implemented => development => [testing](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests) => unstable (_practical testing_) => stable

### Implemented


| Function                 | Module                                     | Usage                                                                                                | State    |
|:-------------------------|:-------------------------------------------|:-----------------------------------------------------------------------------------------------------|:---------|
| **Base**                 | ansibleguy.opnsense.list                   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_list.md)               | stable   |
| **Base**                 | ansibleguy.opnsense.reload                 | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md)             | stable |
| **Alias**                | ansibleguy.opnsense.alias                  | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md)              | stable | 
| **Alias**                | ansibleguy.opnsense.alias_multi            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md)        | stable |
| **Alias**                | ansibleguy.opnsense.alias_purge            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md)        | stable |
| **Rules**                | ansibleguy.opnsense.rule                   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md)               | unstable |
| **Rules**                | ansibleguy.opnsense.rule_multi             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)         | unstable |
| **Rules**                | ansibleguy.opnsense.rule_purge             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)         | unstable |
| **Savepoints**           | ansibleguy.opnsense.savepoint              | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_savepoint.md)          | unstable |
| **Packages**             | ansibleguy.opnsense.package                | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md)            | stable |
| **System**               | ansibleguy.opnsense.system                 | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_system.md)             | unstable |
| **Cron-Jobs**            | ansibleguy.opnsense.cron                   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_cron.md)               | unstable |
| **Routes**               | ansibleguy.opnsense.route                  | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_route.md)              | unstable |
| **DNS Forwarding**       | ansibleguy.opnsense.unbound_forward        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_forwarding.md) | stable |
| **DNS over TLS**         | ansibleguy.opnsense.unbound_dot            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_dot.md)        | stable |
| **DNS Host overrides**   | ansibleguy.opnsense.unbound_host           | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host.md)       | stable |
| **DNS Domain overrides** | ansibleguy.opnsense.unbound_domain         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_domain.md)     | unstable |
| **DNS Host-Aliases**     | ansibleguy.opnsense.unbound_host_alias     | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host_alias.md) | unstable |
| **Syslog**               | ansibleguy.opnsense.syslog                 | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_syslog.md)             | stable |
| **IPSec Certificates**   | ansibleguy.opnsense.ipsec_cert             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_ipsec.md)              | unstable |
| **Traffic Shaper**       | ansibleguy.opnsense.shaper_pipe            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_shaper.md)             | unstable |
| **Traffic Shaper**       | ansibleguy.opnsense.shaper_queue           | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_shaper.md)             | unstable |
| **Traffic Shaper**       | ansibleguy.opnsense.shaper_rule            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_shaper.md)             | unstable |
| **Monit**                | ansibleguy.opnsense.monit_service          | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md)              | unstable |
| **Monit**                | ansibleguy.opnsense.monit_alert            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md)              | unstable |
| **Monit**                | ansibleguy.opnsense.monit_test             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md)              | unstable |
| **WireGuard**            | ansibleguy.opnsense.wireguard_server       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md)          | unstable |
| **WireGuard**            | ansibleguy.opnsense.wireguard_peer         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md)          | unstable |
| **WireGuard**            | ansibleguy.opnsense.wireguard_show         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md)          | unstable |
| **WireGuard**            | ansibleguy.opnsense.wireguard_general      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_wireguard.md)          | unstable |
| **Interfaces**           | ansibleguy.opnsense.interface_vlan         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_interface.md)          | unstable |
| **Interfaces**           | ansibleguy.opnsense.interface_vxlan        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_interface.md)          | unstable |
| **NAT**                  | ansibleguy.opnsense.source_nat             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_source_nat.md)         | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_bfd_general        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bfd.md)            | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_bfd_neighbor       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bfd.md)            | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_bgp_general        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_bgp_neighbor       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_bgp_prefix_list    | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_bgp_route_map      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_bgp_community_list | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_bgp_as_path        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_bgp.md)            | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_diagnostic         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_diagnostic.md)     | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_ospf_general       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_ospf_prefix_list   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_ospf_interface     | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_ospf_network       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_ospf3_general      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |
| **Dynamic Routing**      | ansibleguy.opnsense.frr_ospf3_interface    | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_frr_ospf.md)           | unstable |


### Roadmap

**Core API**:

- [Proxy](https://docs.opnsense.org/development/api/core/proxy.html)
- [IDS](https://docs.opnsense.org/development/api/core/ids.html)
- [~~IPSec~~](https://docs.opnsense.org/development/api/core/ipsec.html) => [not API enabled](https://forum.opnsense.org/index.php?topic=18914.msg146063#msg146063)

**Plugins API**:

- [Zabbix Agent](https://docs.opnsense.org/development/api/plugins/zabbixagent.html)
- [STunnel](https://docs.opnsense.org/development/api/plugins/stunnel.html)
- [Backup](https://docs.opnsense.org/development/api/plugins/backup.html)
- [FreeRadius](https://docs.opnsense.org/development/api/plugins/freeradius.html)
- [Bind](https://docs.opnsense.org/development/api/plugins/bind.html)
- [Zabbix Proxy](https://docs.opnsense.org/development/api/plugins/zabbixproxy.html)

---

## Usage

### Prerequisites

You need to create API credentials as described in [the documentation](https://docs.opnsense.org/development/how-tos/api.html#creating-keys).

**Menu**: System - Access - Users - Edit {admin user} - Add api key

#### SSL Certificate

If you use your firewall for non-testing purposes - you should **ALWAYS USE SSL VERIFICATION** for your connections!

```yaml
ssl_verify: true
```

To make a connection trusted you need either:

- a valid public certificate for the DNS-Name your firewall has (_LetsEncrypt/ACME_)
- an internal certificate authority that is used to create signed certificates
  - you could create such internal certificates using OPNSense. See [documentation](https://docs.opnsense.org/manual/how-tos/self-signed-chain.html).
  - if you do so - it is important that the IP-address and/or DNS-Name of your firewall is included in the 'Subject Alternative Name' (_SAN_) for it to be valid

After you got a valid certificate - you need to import and activate it:
- Import: 'System - Trust - Certificates - Import'
- Make sure your DNS-Names are allowed: 'System - Settings - Administration - Alternate Hostnames'
- Activate: 'System - Settings - Administration - SSL Certificate'

If you are using an internal CA for your certificates - you have to provide its public key to the modules:

```yaml
ssl_ca_file: '/path/to/ca.pem'
```

---

### Basics

#### Defaults

If some parameters will be the same every time - use 'module_defaults':

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.alias:
        firewall: 'opnsense.template.ansibleguy.net'
        api_credential_file: '/home/guy/.secret/opn.key'
        # if you use an internal certificate:
        #   ssl_ca_file: '/etc/ssl/certs/custom/ca.crt'
        # else you COULD (but SHOULD NOT) use:
        #   ssl_verify: false

  tasks:
    - name: Example
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST1'
        content: ['1.1.1.1']
```

#### Inventory

If you are running the modules over hosts in your inventory - you would do it like that:

```yaml
- hosts: firewalls
  connection: local  # execute modules on controller
  gather_facts: no
  tasks:
    - name: Example
      ansibleguy.opnsense.alias:
        firewall: "{{ ansible_host }}"  # or use a per-host variable to store the FQDN..
```

#### Vault

You may want to use '**ansible-vault**' to **encrypt** your 'api_credential_file' or 'api_secret'

```bash
ansible-vault encrypt /path/to/credential/file
# or
ansible-vault encrypt_string 'api_secret'

# run playbook:
ansible-playbook -D opnsense.yml --ask-vault-pass
```

#### Running

These modules support check-mode and can show you the difference between existing and configured items:

```bash
# show difference
ansible-playbook opnsense.yml -D

# run in check-mode (no changes are made)
ansible-playbook opnsense.yml --check
```

---

## Development

See: [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/develop.md)

---

## Errors

If you get error messages - you should at first check if there are any errors listed.

Sometimes the error message can be pretty long, therefore you might want to copy its output into an editor of your choice and Strg+F/search for the terms 'Error:' or '_content'!

Per example:

```bash
# OUTPUT:
fatal: [localhost]: FAILED! => {"changed": false, "msg": "API call failed | Error: {'rule.interface': 'option not in list'} | Response: {'status_code': 200, 'headers': Headers({'content-type': 'application/json; charset=UTF-8', 'content-length': '73', 'date': 'Tue, 30 Aug 2022 15:17:57 GMT', 'server': 'OPNsense'}), '_request': <Request('POST', 'https://FIREWALL/api/firewall/filter/addRule')>, 'next_request': None, 'extensions': {'http_version': b'HTTP/1.1', 'reason_phrase': b'OK', 'network_stream': <httpcore.backends.sync.SyncStream object at 0x7f7efa1975b0>}, 'history': [], 'is_closed': True, 'is_stream_consumed': True, 'default_encoding': 'utf-8', 'stream': <httpx._client.BoundSyncStream object at 0x7f7efa1b28e0>, '_num_bytes_downloaded': 73, '_decoder': <httpx._decoders.IdentityDecoder object at 0x7f7efa139190>, '_elapsed': datetime.timedelta(microseconds=189718), '_content': b'{\"result\":\"failed\",\"validations\":{\"rule.interface\":\"option not in list\"}}', '_encoding': 'UTF-8', '_text': '{\"result\":\"failed\",\"validations\":{\"rule.interface\":\"option not in list\"}}'}"}

# ERROR:
{'rule.interface': 'option not in list'}
```

**Known errors**:

- 'option not in list' => an invalid option was provided for this parameter
- 'port only allowed for tcp/udp' => any protocol except 'TCP' or 'UDP' provided
- 'ConnectionError: Got timeout calling' => you can override the used timeout manually:

  Per example:
  ```yaml
  - name: Example
    ansibleguy.opnsense.alias:
      timeout: 60  # seconds
  ```

**Known issues**:


- **Module-call taking long**

  Many of the modules need to 'apply' its configuration after a change happened.

  Sometimes this 'reload' takes some time as the firewall needs to process some information.

  Per example:

  - URL-Table alias needs to be populated
  - Syslog needs to resolve its DNS-target (_if not able to resolve_)
  
  **What to do about it?**

  If you are calling a module **in a loop** for multiple items - it might be faster to use the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md) instead.
