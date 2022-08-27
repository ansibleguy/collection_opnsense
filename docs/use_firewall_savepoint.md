# OPNSense - Firewall-Savepoint module

**STATE**: testing - early stage

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/firewall_savepoint.yml)

**API DOCS**: [Plugins - Firewall](https://docs.opnsense.org/development/api/plugins/firewall.html)

## Info

You can use those savepoints to prevent lockout-situations when managing rulesets remotely.

Here is the basic process:

![Rollback process](https://docs.opnsense.org/_images/blockdiag-43422f611798118832d099ed58decb1437fb76a0.png)

It currently just works with the 'Firewall' plugin:

- [Firewall - Filter](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md)
- [Firewall - Source NAT](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_snat.md)

## Usage

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.firewall_savepoint:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Create a savepoint for firewall filters
      ansibleguy.opnsense.firewall_savepoint:
        action: 'create'
        controller: 'filter'  # default
      register: filter_savepoint

    - name: Apply savepoint
      ansibleguy.opnsense.firewall_savepoint:
        action: 'apply'
        revision: "{{ filter_savepoint.revision }}"

    - name: Revert savepoint
      ansibleguy.opnsense.firewall_savepoint:
        action: 'revert'
        revision: "{{ filter_savepoint.revision }}"

    - name: Create a savepoint for source-nat filters
      ansibleguy.opnsense.firewall_savepoint:
        action: 'create'
        controller: 'source_nat'
      register: snat_savepoint

    - name: Remove source-nat savepoint (else it will be reverted automatically)
      ansibleguy.opnsense.firewall_savepoint:
        action: 'remove'
        controller: 'source_nat'
        revision: "{{ snat_savepoint.revision }}"
```
