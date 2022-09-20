from socket import socket, AF_INET, SOCK_STREAM
from time import time, sleep

from ansible.module_utils.basic import AnsibleModule


def opn_reachable(module: AnsibleModule) -> bool:
    with socket(AF_INET, SOCK_STREAM) as s:
        return s.connect_ex((
            module.params['firewall'],
            module.params['api_port']
        )) == 0


def wait_for_response(module: AnsibleModule) -> bool:
    timeout = time() + module.params['wait_timeout']

    if module.params['action'] == 'upgrade':
        # waiting longer for download/install to finish
        sleep(int(module.params['wait_timeout'] / 2))

    else:
        # waiting for services to stop
        sleep(10)

    while time() < timeout:
        if opn_reachable(module=module):
            return True

        sleep(module.params['poll_interval'])

    return False
