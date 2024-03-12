# Tests

## Tester dependencies

```bash
python3 -m pip install -r requirements_test.txt
```

## Firewall dependencies

The Firewall used for testing should be a dedicated VM for testing. You can use the official [ova image](https://docs.opnsense.org/manual/how-tos/installova.html).

**THE TESTS WILL OVERRIDE THE EXISTING CONFIG!**

Most tests fail if some other config is found.

### Packages

Some tests need packages to be pre-installed:

* webproxy_* - `os-squid`
* frr_* - `os-frr`
* bind_* - `os-bind`

### Interfaces

Some tests benefit from having a second network-interface available.

You need to add a `opt1` dummy-interface named `TEST`. The assigned IPs do not matter.

### Internet access

To perform some tests (system, ids) the test firewall needs to reach some public service:

* system - `pkg.opnsense.org`
* ids - `rules.emergingthreats.net`

### Certificates

These internal certificates need to be created:

* CA: `OpenVPN`
* Client Certificate: `OpenVPN Client`
* Server Certificate: `OpenVPN Server` - SAN `DNS:openvpn.intern`

----

## Run

### Single module

```bash
bash scripts/test_single.sh
> Arguments:
>   1: firewall
>   2: api key file
>   3: path to local collection - set to '0' to clone from github
>   4: name of test to run
>   5: if check-mode should be ran (optional; 0/1; default=1)
>   6: path to virtual environment (optional)
```

### All modules

```bash
bash scripts/test.sh
> Arguments:
>   1: firewall
>   2: api key file
>   3: path to local collection - set to '0' to clone from github
>   4: path to virtual environment (optional)
```

----

## Automatic tests

The tests are run automatically using the [AnsibleGuy infrastructure](https://github.com/ansibleguy/_meta_cicd)!

It is based on [some bash scripts](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/collection_test.sh.j2) and systemd timers.

Logs for those functional tests can be found here: [Short](https://badges.ansibleguy.net/log/collection_opnsense_test_short.log), [Full](https://badges.ansibleguy.net/log/collection_opnsense_test.log)
