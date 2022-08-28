# OPNSense - Package module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/package.yml)

**API DOCS**: [Core - Firmware](https://docs.opnsense.org/development/api/core/firmware.html)

## Info

If the package cache is too old it will take some time as OPNSense automatically checks for updates beforehand.

## Usage

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.savepoint:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
  
  tasks:
    - name: Installing
      ansibleguy.opnsense.package:
        name: 'os-api-backup'
        action: 'install'

    - name: Removing
      ansibleguy.opnsense.package:
        name: 'os-api-backup'
        action: 'remove'

    - name: Re-installing
      ansibleguy.opnsense.package:
        name: 'os-api-backup'
        action: 'reinstall'

    - name: Locking
      ansibleguy.opnsense.package:
        name: 'os-api-backup'
        action: 'lock'

    - name: Unlocking
      ansibleguy.opnsense.package:
        name: 'os-api-backup'
        action: 'unlock'
```
