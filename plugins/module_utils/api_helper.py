import ssl
from ipaddress import ip_address
from pathlib import Path
from validators import domain

from ansible.module_utils.basic import AnsibleModule


def check_or_load_credentials(module: AnsibleModule):
    if module.params['api_key'] is None and module.params['api_credential_file'] is not None:
        cred_file_info = Path(module.params['api_credential_file'])

        if cred_file_info.is_file():
            cred_file_mode = oct(cred_file_info.stat().st_mode)[-3:]

            if int(cred_file_mode[2]) != 0:
                module.warn(
                    f"Provided 'api_credential_file' at path "
                    f"'{module.params['api_credential_file']}' is world-readable "
                    f"(mode {cred_file_mode})!"
                )

            with open(module.params['api_credential_file'], 'r') as file:
                module.params['api_key'] = file.readline().split('=', 1)[1].strip()
                module.params['api_secret'] = file.readline().split('=', 1)[1].strip()

        else:
            module.fail_json(
                f"Provided 'api_credential_file' at path "
                f"'{module.params['api_credential_file']}' does not exist!"
            )

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
    if not is_ip(module.params['firewall']) and not domain(module.params['firewall']):
        module.fail_json(f"Host '{module.params['firewall']}' is neither a valid IP nor Domain-Name!")


def ssl_verification(module: AnsibleModule) -> (ssl.SSLContext, bool):
    context = ssl.create_default_context()

    if not module.params['ssl_verify']:
        context = False

    elif module.params['ssl_ca_file'] is not None:
        if Path(module.params['ssl_ca_file']).is_file():
            context.load_verify_locations(cafile=module.params['ssl_ca_file'])

        else:
            module.fail_json(f"Provided 'ssl_ca_file' at path '{module.params['ssl_ca_file']}' does not exist!")

    return context


def get_params_path(cnf: dict) -> str:
    params_path = ''

    if 'params' in cnf and cnf['params'] is not None:
        for param in cnf['params']:
            params_path += f"/{param}"

    return params_path


def debug_output(module: AnsibleModule, msg: str):
    if 'debug' in module.params and module.params['debug']:
        module.warn(msg)


def check_response(module: AnsibleModule, cnf: dict, response) -> dict:
    debug_output(module=module, msg=f"RESPONSE: {response.__dict__}")

    if 'allowed_http_stati' not in cnf:
        cnf['allowed_http_stati'] = [200]

    json = response.json()

    if response.status_code not in cnf['allowed_http_stati']:
        if f"{response.__dict__}".find('Controller not found') != -1:
            module.fail_json(
                msg=f"API call failed | Needed plugin not installed! | Response: {response.__dict__}"
            )
        elif f"{response.__dict__}".find('Cannot delete alias. Currently in use') != -1:
            json['in_use'] = True

        else:
            module.fail_json(msg=f"API call failed | Response: {response.__dict__}")

    return json
