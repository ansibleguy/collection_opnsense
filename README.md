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


|Function | Module                          | Usage                                                                                         | State           |
|:---------|:--------------------------------|:----------------------------------------------------------------------------------------------|:----------------|
| **Alias**| ansibleguy.opnsense.alias       | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md)       | unstable        | 
| **Alias** | ansibleguy.opnsense.alias_multi | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md) | unstable        |
| **Alias** | ansibleguy.opnsense.alias_purge | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md) | development     |
| **Rules** | ansibleguy.opnsense.rule        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md)        | unstable        |
| **Rules** | ansibleguy.opnsense.rule_multi  | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)  | unstable        |
| **Rules** | ansibleguy.opnsense.rule_purge  | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md)  | testing         |
| **Savepoints** | ansibleguy.opnsense.savepoint   | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_savepoint.md)   | unstable        |
| **Packages** | ansibleguy.opnsense.package     | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md)     | unstable        |
| **System** | ansibleguy.opnsense.system      | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_system.md)      | unstable        |
| **Source NAT** | ansibleguy.opnsense.snat        | [Docs](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_snat.md)        | not implemented |

### Roadmap

**Core API**:

- [Cron](https://docs.opnsense.org/development/api/core/cron.html)
- [IDS](https://docs.opnsense.org/development/api/core/ids.html)
- [IPSec](https://docs.opnsense.org/development/api/core/ipsec.html)
- [Monit](https://docs.opnsense.org/development/api/core/monit.html)
- [Routes](https://docs.opnsense.org/development/api/core/routes.html)
- [Syslog](https://docs.opnsense.org/development/api/core/syslog.html)
- [Trafficshaper](https://docs.opnsense.org/development/api/core/trafficshaper.html)
- [Unbound](https://docs.opnsense.org/development/api/core/unbound.html)

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

The basic API interaction is handled in 'ansibleguy.opnsense.plugins.module_utils.api'.

It is a generic abstraction layer for interacting with the api - therefore all plugins should be able to function with it!

### Module

There is a [module-template](https://github.com/ansibleguy/collection_opnsense/blob/stable/plugins/modules/_tmpl.py) that can be copied - so you don't have to re-write the basic structure.

### API

One can choose to either:

- create a http-session - faster if multiple calls are needed

  p.e. _check current state => create/update/delete_

  ```python3
  from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
  session = Session(module=module)
  session.get(cnf={'controller': 'alias', 'command': 'addItem', 'data': {'name': 'dummy', ...}})
  session.post(cnf={'controller': 'alias', 'command': 'delItem', 'params': [uuid]})
  session.close()
  ```

- use a single call - if only one is needed

  p.e. toggle a cronjob or restart a service

  ```python3
  from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import single_get, single_post
  single_get(
      module=module, 
      cnf={'controller': 'alias', 'command': 'addItem', 'data': {'name': 'dummy', ...}}
  )
  single_post(
      module=module, 
      cnf={'controller': 'alias', 'command': 'delItem', 'params': [uuid]}
  )
  ```

For the controller/command/params/data definition - check the [OPNSense API Docs](https://docs.opnsense.org/development/api.html#core-api)!


### Debugging

#### Verbose output
If you want to output something to ansible's runtime - use 'module.warn':

```python3
module.warn(f"{before} != {after}")
```

You can also use the 'debug' argument to enable verbose output of the api requests. 

```yaml
- name: Example
  ansibleguy.opnsense.alias:
    debug: true
```

'Multi' modules also support the 'debug' parameter on a per-item basis - so you don't get flooded.

#### Error messages

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
