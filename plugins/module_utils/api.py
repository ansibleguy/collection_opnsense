import httpx

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_helper \
    import check_host, ssl_verification, check_response, get_params_path, debug_output,\
    check_or_load_credentials


class Session:
    def __init__(self, module: AnsibleModule):
        self.m = module
        self.s = self.start()

    def start(self):
        check_host(module=self.m)
        check_or_load_credentials(module=self.m)
        return httpx.Client(
            base_url=f"https://{self.m.params['firewall']}/api",
            auth=(self.m.params['api_key'], self.m.params['api_secret']),
            verify=ssl_verification(module=self.m),
        )

    def get(self, cnf: dict) -> dict:
        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

        debug_output(
            module=self.m,
            msg=f"REQUEST: GET | URL: {self.s.base_url}{call_url}"
        )

        response = check_response(
            module=self.m,
            cnf=cnf,
            response=self.s.get(call_url)
        )

        return response

    def post(self, cnf: dict) -> dict:
        headers = {}
        data = None

        if 'data' in cnf and cnf['data'] is not None and len(cnf['data']) > 0:
            headers = {'Content-Type': 'application/json'}
            data = cnf['data']

        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

        debug_output(
            module=self.m,
            msg=f"REQUEST: POST | "
                f"HEADERS: '{headers}' | "
                f"URL: {self.s.base_url}{call_url} | "
                f"DATA: {data}"
        )

        response = check_response(
            module=self.m,
            cnf=cnf,
            response=self.s.post(call_url, json=data, headers=headers)
        )

        return response

    def close(self):
        self.s.close()


def single_get(module: AnsibleModule, cnf: dict) -> dict:
    check_host(module=module)
    params_path = get_params_path(cnf=cnf)
    call_url = f"https://{module.params['firewall']}/api/" \
               f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

    debug_output(
        module=module,
        msg=f"REQUEST: GET | URL: {call_url}"
    )

    check_or_load_credentials(module=module)
    response = check_response(
        module=module,
        cnf=cnf,
        response=httpx.get(
            call_url,
            auth=(module.params['api_key'], module.params['api_secret']),
            verify=ssl_verification(module=module),
        )
    )

    return response


def single_post(module: AnsibleModule, cnf: dict) -> dict:
    headers = {}
    check_host(module=module)
    data = None

    if 'data' in cnf and cnf['data'] is not None and len(cnf['data']) > 0:
        headers = {'Content-Type': 'application/json'}
        data = cnf['data']

    params_path = get_params_path(cnf=cnf)
    call_url = f"https://{module.params['firewall']}/api/" \
               f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

    debug_output(
        module=module,
        msg=f"REQUEST: POST | "
            f"HEADERS: '{headers}' | "
            f"URL: {call_url} | "
            f"DATA: {data}"
    )

    check_or_load_credentials(module=module)
    response = check_response(
        module=module,
        cnf=cnf,
        response=httpx.post(
            call_url,
            auth=(module.params['api_key'], module.params['api_secret']), verify=ssl_verification(module=module),
            json=data, headers=headers,
        )
    )

    return response
