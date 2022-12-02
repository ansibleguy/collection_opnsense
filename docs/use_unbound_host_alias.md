# OPNSense - DNS host-alias module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/unbound_host_alias.yml)

**API DOCS**: [Core - Unbound](https://docs.opnsense.org/development/api/core/unbound.html)

**BASE DOCS**: [Unbound](https://docs.opnsense.org/manual/unbound.html)

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

| Parameter    | Type   | Required | Default value | Aliases   | Comment                                                                                                                                                                                                                        |
|:-------------|:-------|:---------|:--------------|:----------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields | string | false    | ['alias', 'domain']              | -         | Fields that are used to match configured domain-overrides with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'hostname', 'domain', 'alias',  'description' |
| alias        | string | true     | -             | hostname  | Host-alias to create                                                                                                                                                                                                           |
| domain       | string | true     | -             | dom, d    | Domain to override                                                                                                                                                                                                             |
| target       | string | false for state changes, else true     | -             | tgt, host | Existing host override record                                                                                                                                                                                                  |
| description  | string | false    | -             | desc      | Optional description for the host-alias. Could be used as unique-identifier when set as only 'match_field'.                                                                                                                    |
| reload       | boolean | false    | true                 | -         | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

## Info

This module manages DNS host-alias override configuration that can be found in the WEB-UI menu: 'Services - Unbound DNS - Overrides - Host overrides - Aliases'

Entries like these override individual results from the forwarders.

Use these for changing DNS results or for adding custom DNS records.

Keep in mind that all resource record types (i.e. A, AAAA, MX, etc. records) of a specified host below are being overwritten.

## Usage

First you will have to know about **alias-matching**.

The module somehow needs to link the configured and existing host-aliases to manage them.

You can to set how this matching is done by setting the 'match_fields' parameter!

The default behaviour is that a host-alias is matched by its 'alias' and 'domain' fields.

However - it is **recommended** to use/set 'description' as **unique identifier** if many aliases are used.

### Mass manage

If you are mass-managing DNS records or using DNS-Blocklists - you might want to disable ```reload: false``` on single module-calls!

This takes a long time, as the service gets reloaded every time!

You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md)


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.unbound_host_alias:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      match_fields: ['description']

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'unbound_host_alias'

  tasks:
    - name: Example
      ansibleguy.opnsense.unbound_host_alias:
        alias: 'test'
        domain: 'opnsense.template.ansibleguy.net'
        target: 'host.opnsense.template.ansibleguy.net'
        # match_fields: ['description']
        # description: 'example'
        # state: 'present'
        # enabled: true
        # debug: false

    - name: Adding alias 'test1.local' for record 'test.local'
      ansibleguy.opnsense.unbound_host_alias:
        alias: 'test1'
        domain: 'local'
        target: 'test.local'
        description: 'test1'
        # match_fields: ['description']

    - name: Disabling
      ansibleguy.opnsense.unbound_host_alias:
        alias: 'test1'
        domain: 'local'
        target: 'test.local'
        description: 'test1'
        enabled: false
        # match_fields: ['description']

    - name: Removing
      ansibleguy.opnsense.unbound_host_alias:
        alias: 'test1'
        domain: 'local'
        target: 'test.local'
        state: 'absent'
        description: 'test1'
        # match_fields: ['description']

    - name: Listing aliases
      ansibleguy.opnsense.list:
      #  target: 'unbound_host_alias'
      register: existing_entries

    - name: Printing entries
      ansible.builtin.debug:
        var: existing_entries.data
```
