# OPNSense - DNS-over-TLS module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/unbound_dot.yml)

**API DOCS**: [Core - Unbound](https://docs.opnsense.org/development/api/core/unbound.html)

**BASE DOCS**: [Unbound](https://docs.opnsense.org/manual/unbound.html)

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

| Parameter  | Type    | Required | Default value | Aliases                   | Comment                                                                                                                                                  |
|:-----------|:--------|:---------|:---------------|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| domain     | string  | true     | -            | dom, d                    | Domain of the DNS-over-TLS entry                                                                                                                         |
| target   | string | true    | -            | server, srv, tgt          | DNS target server                                                                                                                                        |
| port | string     | false    | 53          | p                         | DNS port of the target server                                                                                                                            |
| verify | string  | false    | -             | common_name, cn, hostname | Verify if CN in certificate matches this value, **if not set - certificate verification will not be performed**! Must be a valid IP-Address or hostname. |
| reload       | boolean | false    | true                 | -                         | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it manually after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |


## Info

This module manages DNS-over-TLS configuration that can be found in the WEB-UI menu: 'Services - Unbound DNS - DNS over TLS'

## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.unbound_dot:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'unbound_dot'

  tasks:
    - name: Example
      ansibleguy.opnsense.unbound_dot:
        domain: 'dot.template.ansibleguy.net'
        target: '1.1.1.1'
        # port: 53
        # verify: 'dot.template.ansibleguy.net'
        # state: 'present'
        # enabled: true
        # debug: false

    - name: Adding
      ansibleguy.opnsense.unbound_dot:
        domain: 'dot.template.ansibleguy.net'
        target: '1.1.1.1'
        verify: 'dot.template.ansibleguy.net'

    - name: Listing dots
      ansibleguy.opnsense.list:
      #  target: 'unbound_dot'
      register: existing_entries

    - name: Printing DNS-over-TLS entries
      ansible.builtin.debug:
        var: existing_entries.data
```
