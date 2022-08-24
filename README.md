# Ansible Collection - ansibleguy.opnsense

### ROLE IN EARLY DEVELOPMENT - DO NOT USE IN PRODUCTION!!

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
ansible-galaxy collection install ansibleguy.opnsense
```


## Usage

### Aliases

```yaml
- hosts: localhost
  tasks:
    - name: Adding a simple alias
      ansibleguy.opnsense.alias:
        host: 'opnsense.template.ansibleguy.net'
        api_credential_file: '/home/guy/.secret/opn.key'
        name: 'ANSIBLE_TEST1'
        description: 'just a test'
        values: ['1.1.1.1']
        state: 'present'
        # type: 'host'  # default
        # ssl_ca_file: '/etc/ssl/certs/custom/ca.crt'
        # ssl_verify: False
        # api_key: !vault ...  # alternative to 'api_credential_file'
        # api_secret: !vault ...

```


## Development

The basic API interaction is handled in 'ansibleguy.opnsense.plugins.module_utils.api_base'.

I kept is pretty generic - therefore all plugins should be able to function with it!

One can choose to either:

- create a http-session - faster if multiple calls are needed

  p.e. _check current state => create/update/delete_)


- use a single call - if only one is needed

  p.e. toggle a cronjob or restart a service


For simplicity - the base functions only use the 'params' of the AnsibleModule object for their config.
