# OPNSense - Rule module

**STATE**: not yet implemented

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/rule.yml)

**API DOCS**: [Plugins - Firewall](https://docs.opnsense.org/development/api/plugins/firewall.html)

## Prerequisites

You need to install the following plugin as OPNSense has no core-api for managing its firewall rules:
```
os-firewall
```

You can also install it using the [package module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md).

## Info

You can prevent lockout-situations using the savepoint systems:

- [Firewall - Savepoint](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_firewall_savepoint.md)

These rules are shown in the separate WEB-UI table.

Menu: 'Firewall - Automation - Source NAT'

## Usage

```yaml
-
```
