from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, gaierror
from time import time, sleep
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session, HTTPX_EXCEPTIONS
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

    _wait_msg(module, 'Waiting for services to stop..')
    sleep(10)

    while time() < timeout:
        poll_interval_start = time()

        if _opn_reachable(module=module):
            _wait_msg(module, 'Got response!')
            return True

        _wait_msg(module, 'Waiting for response..')
        poll_interval_elapsed = time() - poll_interval_start
        if poll_interval_elapsed < module.params['poll_interval']:
            sleep(module.params['poll_interval'] - poll_interval_elapsed)

    raise TimeoutError


def wait_for_update(module: AnsibleModule, s: Session) -> bool:
    timeout = time() + module.params['wait_timeout']

    if module.params['action'] == 'upgrade':
        _wait_msg(module, 'Waiting for download & upgrade to finish..')

    else:
        _wait_msg(module, 'Waiting for update to finish..')

    sleep(2)

    while time() < timeout:
        poll_interval_start = time()

        try:
            result = s.get({
                'command': 'upgradestatus',
                'module': 'core',
                'controller': 'firmware',
            })
            status = result['status']

            _wait_msg(module, f"Got response: {status}")

            if status == 'error' and 'log' in result:
                _wait_msg(module, f"Got error: {result['log']}")
                return False

            if status == 'done':
                _wait_msg(module, f"Got result: {result['log']}")
                return True

        except (HTTPX_EXCEPTIONS, ConnectionError, TimeoutError):
            # not reachable while rebooting
            _wait_msg(module, 'Waiting for response..')

        poll_interval_elapsed = time() - poll_interval_start
        if poll_interval_elapsed < module.params['poll_interval']:
            sleep(module.params['poll_interval'] - poll_interval_elapsed)

    raise TimeoutError
