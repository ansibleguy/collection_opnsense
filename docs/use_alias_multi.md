# OPNSense - Multi-Alias module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias_multi.yml) | [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias_purge.yml)

**API DOCS**: [Core - Firewall](https://docs.opnsense.org/development/api/core/firewall.html)

This module allows you to manage multiple aliases.

It is faster than the 'alias' module as it reduces the needed api/http calls.

## Info

For more detailed information on what alias types are supported - see [the documentation](https://docs.opnsense.org/manual/aliases.html).

## Multi

- Each alias has the attributes as defined in the [alias](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md) module

- To ensure valid configuration - the attributes of each alias get verified using ansible's built-in verifier

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

### ansibleguy.opnsense.alias_multi

| Parameter | Type       | Required | Default value | Aliases | Comment                                                    |
|:----------|:-----------|:---------|:--------------|:--------|:-----------------------------------------------------------|
| aliases      | dictionary | true     | -             | -       | Dictionary of aliases to manage/configure                  |
| fail_verification      | boolean    | false    | false         | fail    | Fail module if single alias fails the verification         |
| state | string      | false   | 'present'     | -       | Options: 'present', 'absent'                               |
| enabled | boolean     | false | true          | -       | If all aliases should be en- or disabled                   |
| output_info | boolean     | false | false         | info    | Enable to show some information on processing at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'. |


For alias parameters see: [Alias](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md#definition)

### ansibleguy.opnsense.alias_purge

| Parameter | Type       | Required | Default value | Aliases | Comment                                                                                                                    |
|:----------|:-----------|:---------|:--------------|:--------|:---------------------------------------------------------------------------------------------------------------------------|
| aliases      | dictionary | true     | -             | -       | Configured aliases - to exclude from purging                                                                               |
| output_info | boolean    | false | false         | info    | Enable to show some information on processing at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'. |
| action | string     | false | 'delete'      | -       | What to do with the matched aliases. One of: 'disable', 'delete'                                                           |
| filters | dictionary | false | -             | -       | Field-value pairs to filter on - per example: {type: port} - to only purge aliases of type 'port'                          |
| filter_invert | boolean | false | false         | -       | If true - it will purge all but the filtered ones                                                                          |
| filter_partial | boolean | false | false         | -       | If true - the filter will also match if it is just a partial value-match                                                   |
| force_all | boolean | false | false         | -       | If set to true and neither aliases, nor filters are provided - all non-builtin aliases will be purged                      |


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.alias_multi:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.alias_list:
      firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
      api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

    ansibleguy.opnsense.alias_purge:
      firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
      api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

  tasks:
    - name: Creation
      ansibleguy.opnsense.alias_multi:
        fail_verification: true  # default = false; Fail module if single alias fails the verification
        aliases:
          test1:
            content: '1.1.1.1'
          test2:
            content: ['1.1.1.1', '1.1.1.2']
            description: 'to be deleted'
          test3:
            type: 'network'
            content: '10.0.0.0/24'
            description: 'to be disabled'

    - name: Changes
      ansibleguy.opnsense.alias_multi:
        aliases:
          test1:
            content: ['1.1.1.3']
          test2:
            state: 'absent'
          test3:
            enabled: false

    - name: Change state of all
      ansibleguy.opnsense.alias_multi:
        aliases:
          test1:
          test3:
        state: 'absent'
        # enabled: true

    - name: Listing
      ansibleguy.opnsense.alias_list:
      register: existing_entries

    - name: Printing aliases
      ansible.builtin.debug:
        var: existing_entries.aliases

    - name: Purging all non-configured aliases
      ansibleguy.opnsense.alias_purge:
        aliases: {...}
        # action: 'disable'  # default = remove

    - name: Purging all port aliases
      ansibleguy.opnsense.alias_purge:
        filters:  # filtering aliases to purge by alias-parameters
          type: 'port'
        # filter_invert: true  # purge all non-port aliases
```
