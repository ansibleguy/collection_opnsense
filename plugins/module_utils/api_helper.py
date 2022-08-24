import ssl
from ipaddress import ip_address
from validators import domain
from pathlib import Path

from ansible.module_utils.basic import AnsibleModule


def check_or_load_credentials(module: AnsibleModule):
    if module.params['api_key'] is None and module.params['api_credential_file'] is not None:
        cred_file_info = Path(module.params['api_credential_file'])

        if cred_file_info.is_file():
            cred_file_mode = oct(cred_file_info.stat().st_mode)[-3:]

            if int(cred_file_mode[2]) != 0:
                module.warn(f"Provided 'api_credential_file' at path '{module.params['api_credential_file']}' is world-readable (mode {cred_file_mode})!")

            with open(module.params['api_credential_file'], 'r') as file:
                module.params['api_key'] = file.readline().split('=', 1)[1].strip()
                module.params['api_secret'] = file.readline().split('=', 1)[1].strip()

        else:
            module.fail_json(f"Provided 'api_credential_file' at path '{module.params['api_credential_file']}' does not exist!")

    elif module.params['api_key'] is None and module.params['api_secret'] is None:
        module.fail_json("Neither 'api_key' & 'api_secret' nor 'api_credential_file' were provided!")


def is_ip(host: str) -> bool:
    valid_ip = False

    try:
        ip_address(host)
        valid_ip = True

    except ValueError:
        pass

    return valid_ip


def check_host(module: AnsibleModule) -> None:
    if not is_ip(module.params['host']) and not domain(module.params['host']):
        module.fail_json(f"Host '{module.params['host']}' is neither a valid IP nor Domain-Name!")


def ssl_verification(module: AnsibleModule) -> (ssl.SSLContext, bool):
    context = ssl.create_default_context()

    if not module.params['ssl_verify']:
        context = False

    elif module.params['ssl_ca_file'] is not None:
        context.load_verify_locations(cafile=module.params['ssl_ca_file'])

    return context


def check_response(module: AnsibleModule, call_config: dict, response: dict) -> dict:
    if ('status' in response and response['status'] not in call_config['allowed_http_stati']) or \
            ('result' in response and response['result'] == 'failed'):
        msg1 = f" => '{response['message']}'" if 'message' in response else ''
        msg2 = f" with response: {response['status']}{msg1}" if 'status' in response else ''
        module.fail_json(msg=f"API call failed{msg2} | Raw response: {response}")
    return response


def get_params_path(call_config: dict) -> str:
    params_path = ''

    if call_config['params'] is not None:
        for param in call_config['params']:
            params_path += f"/{param}"

    return params_path
