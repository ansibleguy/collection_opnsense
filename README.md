# Ansible Collection - ansibleguy.opnsense

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
# or
ansible-galaxy install -r ansibleguy_opnsense.yml
```


## Usage

### Prerequisites

You need to create API credentials as described in [the documentation](https://docs.opnsense.org/development/how-tos/api.html#creating-keys).

**Menu**: System - Access - Users - Edit {admin user} - Add api key

### Basics

If some parameters will be the same every time - use 'module_defaults':

```yaml
- hosts: localhost
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

### Alias

See: [Usage](https://github.com/ansibleguy/collection_opnsense/blob/stable/use_alias.md)

State: stable

### Multi-Alias

Faster if you need/want to mass-manage aliases.

See: [Usage](https://github.com/ansibleguy/collection_opnsense/blob/stable/use_multi_alias.md)

State: unstable

## Development

The basic API interaction is handled in 'ansibleguy.opnsense.plugins.module_utils.api_base'.

I kept is pretty generic - therefore all plugins should be able to function with it!

One can choose to either:

- create a http-session - faster if multiple calls are needed

  p.e. _check current state => create/update/delete_)

  ```python3
  from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_base import Session
  session = Session(module=module)
  session.get(call_config={'controller': 'alias', 'command': 'addItem', 'data': {'name': 'dummy', ...}})
  session.post(call_config={'controller': 'alias', 'command': 'delItem', 'params': [uuid]})
  session.close()
  ```

- use a single call - if only one is needed

  p.e. toggle a cronjob or restart a service

  ```python3
  from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_base import single_get, single_post
  single_get(
      module=module, 
      call_config={'controller': 'alias', 'command': 'addItem', 'data': {'name': 'dummy', ...}}
  )
  single_post(
      module=module, 
      call_config={'controller': 'alias', 'command': 'delItem', 'params': [uuid]}
  )
  ```

For the controller/command/params/data definition - check the [OPNSense API Docs](https://docs.opnsense.org/development/api.html#core-api)!


### Debugging

If you want to output something to ansible's runtime - use 'module.warn':

```python3
module.warn(f"{before} != {after}")
```

You can also add the 'debug' argument to the modules to allow verbose output for the api requests. 

```python3
module_args = dict(
    debug=dict(type='bool', required=False, default=False),
    ...
)
```

