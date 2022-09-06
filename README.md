# Ansible Collection - ansibleguy.opnsense

[![Functional Test Status](https://badges.ansibleguy.net/opnsense.collection.test.svg)](https://github.com/ansibleguy/collection_opnsense/blob/stable/scripts/test.sh)
[![Lint Test Status](https://badges.ansibleguy.net/opnsense.collection.lint.svg)](https://github.com/ansibleguy/collection_opnsense/blob/stable/scripts/lint.sh)

---

## Contribute

Feel free to contribute to this project using [pull-requests](https://github.com/ansibleguy/collection_opnsense/pulls), [issues](https://github.com/ansibleguy/collection_opnsense/issues) and [discussions](https://github.com/ansibleguy/collection_opnsense/discussions)!

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


| Function                 | Module                                      | Usage                                                                                                | State    |
|:-------------------------|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------|:---------|
| **Alias**                | ansibleguy.opnsense.alias                   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md)              | unstable | 
| **Alias**                | ansibleguy.opnsense.alias_multi             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md)        | unstable |
| **Alias**                | ansibleguy.opnsense.alias_purge             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md)        | unstable |
| **Alias**                | ansibleguy.opnsense.alias_list              | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md)        | unstable |
| **Rules**                | ansibleguy.opnsense.rule                    | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md)               | unstable |
| **Rules**                | ansibleguy.opnsense.rule_multi              | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)         | unstable |
| **Rules**                | ansibleguy.opnsense.rule_purge              | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)         | unstable |
| **Rules**                | ansibleguy.opnsense.rule_list               | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)         | unstable |
| **Savepoints**           | ansibleguy.opnsense.savepoint               | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_savepoint.md)          | unstable |
| **Packages**             | ansibleguy.opnsense.package                 | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md)            | unstable |
| **System**               | ansibleguy.opnsense.system                  | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_system.md)             | unstable |
| **Cron-Jobs**            | ansibleguy.opnsense.cron                    | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_cron.md)               | unstable |
| **Routes**               | ansibleguy.opnsense.route                   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_route.md)              | unstable |
| **DNS Forwarding**       | ansibleguy.opnsense.unbound_forward         | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_forwarding.md) | unstable  |
| **DNS Forwarding**       | ansibleguy.opnsense.unbound_forward_list    | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_forwarding.md) | unstable |
| **DNS over TLS**         | ansibleguy.opnsense.unbound_dot             | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_dot.md)        | unstable |
| **DNS over TLS**         | ansibleguy.opnsense.unbound_dot_list        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_dot.md)        | unstable |
| **DNS Host overrides**   | ansibleguy.opnsense.unbound_host            | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host.md)       | unstable |
| **DNS Host overrides**   | ansibleguy.opnsense.unbound_host_list       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host.md)       | unstable |
| **DNS Domain overrides** | ansibleguy.opnsense.unbound_domain          | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_domain.md)     | unstable |
| **DNS Domain overrides** | ansibleguy.opnsense.unbound_domain_list     | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_domain.md)     | unstable |
| **DNS Host-Aliases**     | ansibleguy.opnsense.unbound_host_alias      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host_alias.md) | testing  |
| **DNS Host-Aliases**     | ansibleguy.opnsense.unbound_host_alias_list | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host_alias.md) | testing  |


### Roadmap

**Core API**:

- [IDS](https://docs.opnsense.org/development/api/core/ids.html)
- [IPSec](https://docs.opnsense.org/development/api/core/ipsec.html)
- [Monit](https://docs.opnsense.org/development/api/core/monit.html)
- [Syslog](https://docs.opnsense.org/development/api/core/syslog.html)
- [Trafficshaper](https://docs.opnsense.org/development/api/core/trafficshaper.html)

**Plugins API**:

- [Backup](https://docs.opnsense.org/development/api/plugins/backup.html)
- [WireGuard](https://docs.opnsense.org/development/api/plugins/wireguard.html)
- [Zabbix Agent](https://docs.opnsense.org/development/api/plugins/zabbixagent.html)
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
