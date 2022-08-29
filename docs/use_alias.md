# OPNSense - Alias module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias.yml)

**API DOCS**: [Core - Firewall](https://docs.opnsense.org/development/api/core/firewall.html)

This module allows you to manage single aliases.


## Info

For more detailed information on what alias types are supported - see [the documentation](https://docs.opnsense.org/manual/aliases.html).

### Mass-Manage

If you want to mass-manage aliases - take a look at the [multi_alias](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_multi_alias.md) module. It is scales better for that use-case!


## Usage

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.alias:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.alias_list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST1'
        description: 'just a test'
        content: '1.1.1.1'
        state: 'present'
        # type: 'host'  # default
        # ssl_ca_file: '/etc/ssl/certs/custom/ca.crt'
        # ssl_verify: False
        # api_key: !vault ...  # alternative to 'api_credential_file'
        # api_secret: !vault ...
        # debug: false

    - name: Adding
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST2'
        content: '192.168.1.1'

    - name: Listing
      ansibleguy.opnsense.alias_list:
      register: existing_aliases
      
    - name: Printing aliases
      ansible.builtin.debug:
        var: existing_aliases.aliases

    - name: Changing
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST2'
        content: ['192.168.1.5', '192.168.10.4']

    - name: Removing
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST3'
        state: 'absent'

    - name: Disabling
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST2'
        enabled: false
```
