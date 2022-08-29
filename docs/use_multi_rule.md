# OPNSense - Rule module

**STATE**: testing

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/rule.yml)

**API DOCS**: [Plugins - Firewall](https://docs.opnsense.org/development/api/plugins/firewall.html)

## Prerequisites

You need to install the following plugin as OPNSense has no core-api for managing its firewall rules:
```
os-firewall
```

You can also install it using the [package module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md).

## Limitations

This plugin has some limitations you need to know of!

See: [rule](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md#limitations)

## Info

**Config**:

- Each rule has the attributes as defined in the [rule](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md) module

- To ensure valid configuration - the attributes of each rule get verified using ansible's built-in verifier

