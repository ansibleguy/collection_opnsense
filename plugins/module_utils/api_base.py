import httpx

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_helper import check_host, ssl_verification, check_response, get_params_path


class Session:
    def __init__(self, module: AnsibleModule):
        self.m = module
        self.s = self.start()

    def start(self):
        check_host(module=self.m)
        return httpx.Client(
            base_url=f"https://{self.m.params['host']}/api",
            auth=(self.m.params['api_key'], self.m.params['api_secret']),
            verify=ssl_verification(module=self.m),
        )

    def get(self, call_config: dict) -> dict:
        params_path = get_params_path(call_config=call_config)
        return check_response(
            module=self.m,
            call_config=call_config,
            response=self.s.get(f"/{call_config['module']}/{call_config['controller']}/{call_config['command']}{params_path}").json()
        )

    def post(self, call_config: dict) -> dict:
        headers = {}

        if call_config['data'] is not None and len(call_config['data']) > 0:
            headers = {'Content-Type': 'application/json'}

        params_path = get_params_path(call_config=call_config)

        return check_response(
            module=self.m,
            call_config=call_config,
            response=self.s.post(
                f"/{call_config['module']}/{call_config['controller']}/{call_config['command']}{params_path}",
                data=call_config['data'], headers=headers,
            ).json()
        )

    def close(self):
        self.s.close()


def single_get(module: AnsibleModule, call_config: dict) -> dict:
    check_host(module=module)
    params_path = get_params_path(call_config=call_config)
    return check_response(
        module=module,
        call_config=call_config,
        response=httpx.get(
            f"https://{call_config['host']}/api/{call_config['module']}/{call_config['controller']}/{call_config['command']}{params_path}",
            auth=(call_config['api_key'], call_config['api_secret']),
            verify=ssl_verification(module=module),
        ).json()
    )


def single_post(module: AnsibleModule, call_config: dict) -> dict:
    headers = {}
    check_host(module=module)

    if call_config['data'] is not None and len(call_config['data']) > 0:
        headers = {'Content-Type': 'application/json'}

    params_path = get_params_path(call_config=call_config)

    return check_response(
        module=module,
        call_config=call_config,
        response=httpx.post(
            f"https://{call_config['host']}/api/{call_config['module']}/{call_config['controller']}/{call_config['command']}{params_path}",
            auth=(call_config['api_key'], call_config['api_secret']), verify=ssl_verification(module=module),
            data=call_config['data'], headers=headers,
        ).json()
    )
