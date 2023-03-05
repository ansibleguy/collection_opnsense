import ssl
from pathlib import Path
from json import JSONDecodeError
from json import dumps as json_dumps
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
    DEBUG_CONFIG
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    ensure_list, is_ip
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_valid_domain


def _load_credential_file(module: AnsibleModule) -> None:
    cred_file_info = Path(module.params['api_credential_file'])

    if cred_file_info.is_file():
        cred_file_mode = oct(cred_file_info.stat().st_mode)[-3:]

        if int(cred_file_mode[2]) != 0:
            module.warn(
                f"Provided 'api_credential_file' at path "
                f"'{module.params['api_credential_file']}' is world-readable "
                f"(mode {cred_file_mode})!"
            )

        with open(module.params['api_credential_file'], 'r', encoding='utf-8') as file:
            config = {}
            vaulted = False

            for line in file.readlines():
                try:
                    key, value = line.split('=', 1)
                    config[key] = value.strip()

                except ValueError:
                    if line.startswith('$ANSIBLE_VAULT'):
                        vaulted = True
                        break

            if vaulted:
                module.fail_json(
                    f"Credential file '{module.params['api_credential_file']}' "
                    'is ansible-vault encrypted! This is not yet supported.'
                )

            if 'key' not in config or 'secret' not in config:
                module.fail_json(
                    f"Credential file '{module.params['api_credential_file']}' "
                    'could not be parsed!'
                )

            module.params['api_key'] = config['key']
            module.params['api_secret'] = config['secret']

    else:
        module.fail_json(
            f"Provided 'api_credential_file' at path "
            f"'{module.params['api_credential_file']}' does not exist!"
        )


def check_or_load_credentials(module: AnsibleModule) -> None:
    if module.params['api_credential_file'] is not None:
        _load_credential_file(module)

    elif module.params['api_key'] is None and module.params['api_secret'] is None:
        module.fail_json("Neither 'api_key' & 'api_secret' nor 'api_credential_file' were provided!")


def check_host(module: AnsibleModule) -> None:
    if not is_ip(module.params['firewall']):
        fw_dns = module.params['firewall']

        if fw_dns.find('.') == -1:
            # TLD-only will fail the domain validation
            fw_dns = f'dummy.{fw_dns}'

        if not is_valid_domain(fw_dns):
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
        for param in ensure_list(cnf['params']):
            params_path += f"/{param}"

    return params_path


def debug_api(
        module: AnsibleModule, method: str = None, url: str = None,
        data: dict = None, headers: dict = None, response: dict = None,
) -> None:
    if 'debug' in module.params and module.params['debug']:
        if response is not None:
            msg = f"RESPONSE: '{response.__dict__}'"

        else:
            msg = f'REQUEST: {method} | URL: {url}'

            if headers is not None:
                msg += f" | HEADERS: '{headers}'"

            if data is not None:
                msg += f" | DATA: '{json_dumps(data)}'"

            log_path = Path(DEBUG_CONFIG['path_log'])
            if not log_path.exists():
                log_path.mkdir()

            with open(
                    f"{log_path}/{DEBUG_CONFIG['log_api_calls']}",
                    'a+', encoding='utf-8'
            ) as log:
                log.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')} | {method} => {url}")

        module.warn(msg)


def check_response(module: AnsibleModule, cnf: dict, response) -> dict:
    debug_api(module=module, response=response)

    if 'allowed_http_stati' not in cnf:
        cnf['allowed_http_stati'] = [200]

    try:
        json = response.json()

    except JSONDecodeError:
        json = {}

    if response.status_code not in cnf['allowed_http_stati'] or \
            ('result' in json and json['result'] == 'failed'):
        # sometimes an error 'hides' behind a 200-code
        if f"{response.__dict__}".find('Controller not found') != -1:
            module.fail_json(
                msg=f"API call failed | Needed plugin not installed! | Response: {response.__dict__}"
            )

        elif f"{response.__dict__}".find('Currently in use') != -1:
            json['in_use'] = True

        else:
            if 'validations' in json:
                module.fail_json(msg=f"API call failed | Error: {json['validations']} | Response: {response.__dict__}")

            else:
                module.fail_json(msg=f"API call failed | Response: {response.__dict__}")

    return json


def api_pretty_exception(method: str, url: str, error) -> ConnectionError:
    call = f'{method} => {url}'
    msg = f"Unable to connect '{call}'!"

    if str(error).find('timed out') != -1:
        msg = f"Got timeout calling '{call}'!"

    return ConnectionError(msg)


def timeout_override(module: AnsibleModule, timeout: float) -> float:
    if 'timeout' in module.params and module.params['timeout'] is not None:
        timeout = module.params['timeout']

    return timeout
