# OPNSense - DNS-Forwarding module

**STATE**: stable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/unbound_forward.yml)

**API DOCS**: [Core - Unbound](https://docs.opnsense.org/development/api/core/unbound.html)

**BASE DOCS**: [Unbound](https://docs.opnsense.org/manual/unbound.html)

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

| Parameter  | Type    | Required | Default value | Aliases          | Comment                       |
|:-----------|:--------|:---------|:---------------|:-----------------|:------------------------------|
| domain     | string  | true     | -            | dom, d           | Domain to forward queries of  |
| target   | string | true    | -            | server, srv, tgt | DNS target server             |
| port | string     | false    | 53          | p                | DNS port of the target server |
| reload       | boolean | false    | true                 | -                | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

## Info

This module manages DNS-Forwardings that can be found in the WEB-UI menu: 'Services - Unbound DNS - Query Forwardings'

### Mass manage

If you are mass-managing DNS records or using DNS-Blocklists - you might want to disable ```reload: false``` on single module-calls!

This takes a long time, as the service gets reloaded every time!

You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md)


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.unbound_forward:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'unbound_forward'

  tasks:
    - name: Example
      ansibleguy.opnsense.unbound_forward:
        domain: 'dot.template.ansibleguy.net'
        target: '1.1.1.1'
        # port: 53
        # verify: 'dot.template.ansibleguy.net'
        # state: 'present'
        # enabled: true
        # debug: false

    - name: Adding
      ansibleguy.opnsense.unbound_forward:
        domain: 'dot.template.ansibleguy.net'
        target: '1.1.1.1'

    - name: Listing forwardings
      ansibleguy.opnsense.list:
      #  target: 'unbound_forward'
      register: existing_entries

    - name: Printing DNS-Forwardings
      ansible.builtin.debug:
        var: existing_entries.data
```
