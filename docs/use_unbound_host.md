# OPNSense - DNS host override module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/unbound_host.yml)

**API DOCS**: [Core - Unbound](https://docs.opnsense.org/development/api/core/unbound.html)

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

### ansibleguy.opnsense.unbound_host

| Parameter  | Type   | Required | Default value | Aliases      | Comment                                                                                                                                                      |
|:-----------|:-------|:---------|:--------------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields     | string | false    | ['hostname', 'domain', 'record_type', 'value', 'prio']              | -            | Fields that are used to match configured host-overrides with the running config - if any of those fields are changed, the module will think it's a new entry |
| hostname     | string | true     | -             | host, h      | Hostname of the record                                                                                                                                       |
| domain     | string | true     | -             | dom, d       | Domain of the record                                                                                                                                         |
| record_type   | string | true     | 'A'           | type, rr, rt | Record type. One of: 'A', 'AAAA', 'MX'                                                                                                                       |
| value   | string | true     | -             | server, mx   | Value the record should hold                                                                                                                                 |
| prio | int    | false    | 10            | mxprio       | Priority that is only used for MX record types                                                                                                               |
| description | string | false    | -             | desc         | Verify if CN in certificate matches this value, **if not set - certificate verification will not be performed**! Must be a valid IP-Address or hostname.     |

### ansibleguy.opnsense.unbound_host_list

Only basic parameters needed.

## Info

This module manages DNS-over-TLS configuration that can be found in the WEB-UI menu: 'Services - Unbound DNS - DNS over TLS'

## Usage

First you will have to know about **host-matching**.

The module somehow needs to link the configured and existing host-overrides to manage them.

You can to set how this matching is done by setting the 'match_fields' parameter!

The default behaviour is that a host-override is matched by its 'hostname', 'domain', 'record_type', 'value' and 'prio' fields.

However - it is **recommended** to use/set 'description' as **unique identifier** if many overrides are used.


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.unbound_host:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      # match_fields: ['description']

    ansibleguy.opnsense.unbound_host_list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.unbound_host:
        hostname: 'host'
        domain: 'opnsense.template.ansibleguy.net'
        value: '192.168.0.1'
        # match_fields: ['description']
        # record_type: 'A'
        # prio: 10
        # description: 'example'
        # state: 'present'
        # enabled: true
        # debug: false

    - name: Adding
      ansibleguy.opnsense.unbound_host:
        hostname: 'host'
        domain: 'opnsense.template.ansibleguy.net'
        value: '192.168.0.1'
        match_fields: ['description']
        description: 'test1'

    - name: Removing
      ansibleguy.opnsense.unbound_host:
        hostname: 'host'
        domain: 'opnsense.template.ansibleguy.net'
        value: '192.168.0.1'
        state: 'absent'
        match_fields: ['description']
        description: 'test1'

    - name: Adding MX record
      ansibleguy.opnsense.unbound_host:
        hostname: 'mx'
        domain: 'opnsense.template.ansibleguy.net'
        value: 'host.opnsense.template.ansibleguy.net'
        record_type: 'MX'
        match_fields: ['description']
        description: 'test2'

    - name: Listing hosts
      ansibleguy.opnsense.unbound_host_list:
      register: existing_host_entries

    - name: Printing entries
      ansible.builtin.debug:
        var: existing_host_entries.hosts
```