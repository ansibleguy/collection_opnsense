# OPNSense - IPSec modules

**STATE**: unstable

**TESTS**: [ipsec_cert](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/ipsec_cert.yml)

**API DOCS**: [Core - IPSec](https://docs.opnsense.org/development/api/core/ipsec.html)

## Limitations

The management of IPSec tunnels [is not yet API available](https://forum.opnsense.org/index.php?topic=18914.0)!

Only its certificates can be managed for now..

## Definition

### ansibleguy.opnsense.ipsec_cert

| Parameter | Type    | Required                         | Default value | Aliases        | Comment                                                                                                                                                                                                                                                                                |
|:----------|:--------|:---------------------------------|:--------------|:---------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name    | string  | true                             | -             | -              | Name of the key-pair - used to identify the entry.                                                                                                                                                                                                                                     |
| public_key      | string | false on delete, true if present | -             | pub_key, pub   | -                                                                                                                                                                                                                                                                                      |
| private_key   | string     | false on delete, true if present                            | -             | priv_key, priv | -                                                                                                                                                                                                                                                                                      |
| type   | string     | false                            | -             | -              | Type of the key. Currently the only option is 'rsa'                                                                                                                                                                                                                                    |
| reload    | boolean  | false                            | 2             | -              | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it manually after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

## Usage

To apply changes to the keys, you need to set 'reload: true' on each call or use the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md) to apply it once you finished modifying all entries!

As far as I can tell - the IPSec service gets restarted one you do so - be aware of that.

### Vault

You may want to use '**ansible-vault**' to **encrypt** your 'private_key' content!

```bash
ansible-vault encrypt_string '-----BEGIN RSA PRIVATE KEY-----\n...-----END RSA PRIVATE KEY-----\n'

# or encrypt the private_key file beforehand (might be easier)
ansible-vault encrypt /path/to/private/key/file.pem
```


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.ipsec_cert:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'ipsec_cert'

  tasks:
    - name: Example
      ansibleguy.opnsense.ipsec_cert:
        name: 'example'
        public_key: |
          -----BEGIN PUBLIC KEY-----
          ...
          -----END PUBLIC KEY-----
        private_key: |
          -----BEGIN RSA PRIVATE KEY-----
          ...
          -----END RSA PRIVATE KEY-----

        # reload: false

    - name: Adding key-pair and applying it
      ansibleguy.opnsense.ipsec_cert:
        name: 'test1'
        public_key: |
          -----BEGIN PUBLIC KEY-----
          ...
          -----END PUBLIC KEY-----
        private_key: !vault ...
        reload: true

    - name: Listing
      ansibleguy.opnsense.list:
      #  target: 'ipsec_cert'
      no_log: true  # could log private keys
      register: existing_entries

    - name: Printing
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Manually reloading/applying config
      ansibleguy.opnsense.reload:
        target: 'ipsec'
```
