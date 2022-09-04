# OPNSense - Firewall-Savepoint module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/savepoint.yml)

**API DOCS**: [Plugins - Firewall](https://docs.opnsense.org/development/api/plugins/firewall.html)

## Info

You can use those savepoints to prevent lockout-situations when managing rulesets remotely.

Here is the basic process:

![Rollback process](https://docs.opnsense.org/_images/blockdiag-43422f611798118832d099ed58decb1437fb76a0.png)

It currently just works with the 'Firewall' plugin:

- [Firewall - Filter](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md)
- [Firewall - Source NAT](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_snat.md)

## Definition

| Parameter | Type   | Required                                                               | Default value | Comment                                                                   |
|:----------|:-------|:-----------------------------------------------------------------------|:--------------|:--------------------------------------------------------------------------|
| name      | string | false                                                                  | 'create'      | Action to execute. One of: 'create', 'revert', 'apply', 'cancel_rollback' |
| revision      | string | false, true if action is one of 'apply', 'revert' or 'cancel_rollback' | -             | Savepoint revision to apply, revert or cancel_rollback                    |
| controller      | string | false                                                                  | 'filter'      | Controller to manage the savepoint of. One of: 'source_nat', 'filter'     |
| api_module      | string | false                                                                  | 'firewall'      | Module to manage the savepoint of. Currently only supports 'firewall'               |

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.savepoint:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Create a savepoint for firewall filters
      ansibleguy.opnsense.savepoint:
        action: 'create'
        controller: 'filter'  # default
      register: filter_savepoint

    - name: Apply savepoint
      ansibleguy.opnsense.savepoint:
        action: 'apply'
        revision: "{{ filter_savepoint.revision }}"

    - name: Revert savepoint
      ansibleguy.opnsense.savepoint:
        action: 'revert'
        revision: "{{ filter_savepoint.revision }}"

    - name: Create a savepoint for firewall source-nat
      ansibleguy.opnsense.savepoint:
        action: 'create'
        controller: 'source_nat'
      register: snat_savepoint

    - name: Remove source-nat savepoint (else it will be reverted automatically)
      ansibleguy.opnsense.savepoint:
        action: 'cancel_rollback'
        controller: 'source_nat'
        revision: "{{ snat_savepoint.revision }}"
```
