# OPNSense - DNS domain override module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/unbound_domain.yml)

**API DOCS**: [Core - Unbound](https://docs.opnsense.org/development/api/core/unbound.html)

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

| Parameter    | Type    | Required | Default value        | Aliases    | Comment                                                                                                                                                                                                                                                                                |
|:-------------|:--------|:---------|:---------------------|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields | string  | false    | ['domain', 'server'] | -          | Fields that are used to match configured domain-overrides with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'domain', 'server', 'description'                                                                     |
| domain       | string  | true     | -                    | dom, d     | Domain to override                                                                                                                                                                                                                                                                     |
| server       | string  | true     | -                    | value, srv | Target server                                                                                                                                                                                                                                                                          |
| description  | string  | false    | -                    | desc       | Optional description for the domain-override. Could be used as unique-identifier when set as only 'match_field'.                                                                                                                                                                       |
| reload       | boolean | false    | true                 | -          | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it manually after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

## Info

This module manages DNS domain-overrides configuration that can be found in the WEB-UI menu: 'Services - Unbound DNS - Overrides - Domain overrides'

Entries like these override an entire domain by specifying an authoritative DNS server to be queried for that domain.

## Usage

First you will have to know about **domain-matching**.

The module somehow needs to link the configured and existing domain-overrides to manage them.

You can to set how this matching is done by setting the 'match_fields' parameter!

The default behaviour is that a domain-override is matched by its 'domain' and 'server' fields.

However - it is **recommended** to use/set 'description' as **unique identifier** if many overrides are used.


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.unbound_domain:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      # match_fields: ['description']

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'unbound_domain'

  tasks:
    - name: Example
      ansibleguy.opnsense.unbound_domain:
        domain: 'opnsense.template.ansibleguy.net'
        server: '192.168.0.1'
        # match_fields: ['description']
        # description: 'example'
        # state: 'present'
        # enabled: true
        # debug: false

    - name: Adding
      ansibleguy.opnsense.unbound_domain:
        domain: 'opnsense.template.ansibleguy.net'
        server: '192.168.0.1'
        match_fields: ['description']
        description: 'test1'

    - name: Disabling
      ansibleguy.opnsense.unbound_domain:
        domain: 'opnsense.template.ansibleguy.net'
        server: '192.168.0.1'
        match_fields: ['description']
        description: 'test1'
        enabled: false

    - name: Removing
      ansibleguy.opnsense.unbound_domain:
        domain: 'opnsense.template.ansibleguy.net'
        server: '192.168.0.1'
        state: 'absent'
        match_fields: ['description']
        description: 'test1'

    - name: Listing domains
      ansibleguy.opnsense.list:
      #  target: 'unbound_domain'
      register: existing_entries

    - name: Printing entries
      ansible.builtin.debug:
        var: existing_entries.data
```
