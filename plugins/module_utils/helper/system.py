from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, gaierror
from time import time, sleep
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import CONNECTION_TEST_TIMEOUT


def _opn_reachable_ipv(module: AnsibleModule, address_family: int) -> bool:
    with socket(address_family, SOCK_STREAM) as s:
        s.settimeout(CONNECTION_TEST_TIMEOUT)
        return s.connect_ex((
            module.params['firewall'],
            module.params['api_port']
        )) == 0


def _opn_reachable(module: AnsibleModule) -> bool:
    try:
        return _opn_reachable_ipv(module, AF_INET)

    except gaierror:
        return _opn_reachable_ipv(module, AF_INET6)


def _wait_msg(module: AnsibleModule, msg: str):
    module.warn(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {msg}")


def wait_for_response(module: AnsibleModule) -> bool:
    timeout = time() + module.params['wait_timeout']

    if module.params['action'] == 'upgrade':
        _wait_msg(module, 'Waiting download & upgrade to finish..')
        sleep(int(module.params['wait_timeout'] / 2))

    else:
        _wait_msg(module, 'Waiting for service to stop..')
        sleep(10)

    while time() < timeout:
        if _opn_reachable(module=module):
            _wait_msg(module, 'Got response!')
            return True

        _wait_msg(module, 'Waiting for response..')
        sleep(module.params['poll_interval'])

    return False
