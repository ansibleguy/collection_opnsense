import socket
import httpx

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.api import \
    check_host, ssl_verification, check_response, get_params_path, debug_output, \
    check_or_load_credentials, raise_pretty_exception

DEFAULT_TIMEOUT = 20.0
HTTPX_EXCEPTIONS = (
    httpx.ConnectTimeout, httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout,
    httpx.TimeoutException, httpx.PoolTimeout,
)


class Session:
    def __init__(self, module: AnsibleModule, timeout: float = DEFAULT_TIMEOUT):
        self.m = module
        self.t = httpx.Timeout(timeout=timeout)
        socket.setdefaulttimeout(timeout)
        self.s = self.start()

    def start(self):
        check_host(module=self.m)
        check_or_load_credentials(module=self.m)
        return httpx.Client(
            base_url=f"https://{self.m.params['firewall']}:{self.m.params['api_port']}/api",
            auth=(self.m.params['api_key'], self.m.params['api_secret']),
            verify=ssl_verification(module=self.m),
            timeout=self.t,
        )

    def get(self, cnf: dict) -> dict:
        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

        debug_output(
            module=self.m,
            msg=f"REQUEST: GET | URL: {self.s.base_url}{call_url}"
        )

        try:
            response = check_response(
                module=self.m,
                cnf=cnf,
                response=self.s.get(url=call_url, timeout=self.t)
            )

        except HTTPX_EXCEPTIONS as error:
            raise_pretty_exception(
                method='GET', error=error,
                url=f'{self.s.base_url}{call_url}',
            )

        return response

    def post(self, cnf: dict, headers: dict = None) -> dict:
        if headers is None:
            headers = {}

        data = None

        if 'data' in cnf and cnf['data'] is not None and len(cnf['data']) > 0:
            headers['Content-Type'] = 'application/json'
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

        try:
            response = check_response(
                module=self.m,
                cnf=cnf,
                response=self.s.post(
                    url=call_url, json=data, headers=headers, timeout=self.t
                )
            )

        except HTTPX_EXCEPTIONS as error:
            raise_pretty_exception(
                method='POST', error=error,
                url=f'{self.s.base_url}{call_url}',
            )

        return response

    def close(self):
        self.s.close()


def single_get(module: AnsibleModule, cnf: dict, timeout: float = DEFAULT_TIMEOUT) -> dict:
    check_host(module=module)
    socket.setdefaulttimeout(timeout)
    params_path = get_params_path(cnf=cnf)
    call_url = f"https://{module.params['firewall']}:{module.params['api_port']}/api/" \
               f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

    debug_output(
        module=module,
        msg=f"REQUEST: GET | URL: {call_url}"
    )

    check_or_load_credentials(module=module)

    try:
        response = check_response(
            module=module,
            cnf=cnf,
            response=httpx.get(
                url=call_url,
                auth=(module.params['api_key'], module.params['api_secret']),
                verify=ssl_verification(module=module),
                timeout=httpx.Timeout(timeout=timeout),
            )
        )

    except HTTPX_EXCEPTIONS as error:
        raise_pretty_exception(method='GET', url=call_url, error=error)

    return response


def single_post(
        module: AnsibleModule, cnf: dict, timeout: float = DEFAULT_TIMEOUT,
        headers: dict = None) -> dict:
    check_host(module=module)
    socket.setdefaulttimeout(timeout)

    if headers is None:
        headers = {}

    data = None

    if 'data' in cnf and cnf['data'] is not None and len(cnf['data']) > 0:
        headers['Content-Type'] = 'application/json'
        data = cnf['data']

    params_path = get_params_path(cnf=cnf)
    call_url = f"https://{module.params['firewall']}:{module.params['api_port']}/api/" \
               f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

    debug_output(
        module=module,
        msg=f"REQUEST: POST | "
            f"HEADERS: '{headers}' | "
            f"URL: {call_url} | "
            f"DATA: {data}"
    )

    check_or_load_credentials(module=module)

    try:
        response = check_response(
            module=module,
            cnf=cnf,
            response=httpx.post(
                url=call_url,
                auth=(module.params['api_key'], module.params['api_secret']), verify=ssl_verification(module=module),
                json=data, headers=headers,
                timeout=httpx.Timeout(timeout=timeout),
            )
        )

    except HTTPX_EXCEPTIONS as error:
        raise_pretty_exception(method='POST', url=call_url, error=error)

    return response
