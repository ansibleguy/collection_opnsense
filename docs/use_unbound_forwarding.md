# OPNSense - DNS-Forwarding module

**STATE**: testing

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/unbound_forward.yml)

**API DOCS**: [Core - Unbound](https://docs.opnsense.org/development/api/core/unbound.html)

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

### ansibleguy.opnsense.unbound_forward

| Parameter  | Type    | Required | Default value | Aliases                   | Comment                                                                                                                                                                                                                                 |
|:-----------|:--------|:---------|:---------------|:--------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| domain     | string  | true     | -            | dom, d                    | Action to execute. One of: 'poweroff', 'reboot', 'update', 'upgrade', 'audit'. **WARNING**: the target firewall will be temporarily unavailable if running action 'upgrade' or 'reboot', or permanently if running action 'poweroff' (; |
| target   | string | true    | -            | server, srv, tgt          | DNS target server                                                                                                                                                                                                                       |
| port | string     | false    | 53          | p                         | DNS port of the target server                                                                                                                                                                                                           |

### ansibleguy.opnsense.unbound_forward_list

Only basic parameters needed.

## Info

This module manages DNS-Forwardings that can be found in the WEB-UI menu: 'Services - Unbound DNS - Query Forwardings'

## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.unbound_forward:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.unbound_forward_list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

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
      ansibleguy.opnsense.unbound_forward_list:
      register: existing_entries

    - name: Printing DNS-Forwardings
      ansible.builtin.debug:
        var: existing_entries.forwardings
```
