# OPNSense - Package module

**STATE**: stable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/package.yml)

**API DOCS**: [Core - Firmware](https://docs.opnsense.org/development/api/core/firmware.html)

**BASE DOCS**: [Plugins](https://docs.opnsense.org/manual/firmware.html#plugins)

## Info

If:

- the package cache is too old, it will take some time - as OPNSense automatically checks for updates beforehand
- the target firewall runs an outdated version, the actions 'install' and 'reinstall' will fail as OPNSense prevents it

  - in that case - you should run '[ansibleguy.opnsense.system](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_system.md)' with action 'upgrade'


Be aware that the list-module with target 'package' will return installed plugins AND base-packages.

## Definition

| Parameter | Type            | Required | Default value | Comment                                                                                           |
|:----------|:----------------|:---------|:--------------|:--------------------------------------------------------------------------------------------------|
| name      | list of strings | true     | -             | Package or list of packages to process                                                            |
| action | string          | true     | -             | Action to execute. One of: 'install', 'reinstall', 'remove', 'lock', 'unlock'                     |
| post_sleep | int             | false    | 3             | Seconds to sleep after executing the action. The firewall needs some time to update package info. |
| timeout | float           | false    | 30.0          | Seconds until the action request times-out                                                        |

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

## Usage

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.package:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
  
    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'package'
  
  tasks:
    - name: Installing
      ansibleguy.opnsense.package:
        name: 'os-api-backup'
        action: 'install'

    - name: Installing - multiple packages at once
      ansibleguy.opnsense.package:
        name: ['os-api-backup', 'os-dmidecode']
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

    - name: Listing
      ansibleguy.opnsense.list:
      #  target: 'package'
      register: existing_entries

    - name: Printing installed packages
      ansible.builtin.debug:
        var: existing_entries.data
```
