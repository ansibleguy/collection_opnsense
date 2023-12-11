from socket import setdefaulttimeout

import httpx

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.api import \
    check_host, ssl_verification, check_response, get_params_path, debug_api, \
    check_or_load_credentials, api_pretty_exception, timeout_override, get_api_retries

DEFAULT_TIMEOUT = 20.0
HTTPX_EXCEPTIONS = (
    httpx.ConnectTimeout, httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout,
    httpx.TimeoutException, httpx.PoolTimeout,
)


class Session:
    def __init__(self, module: AnsibleModule, timeout: float = DEFAULT_TIMEOUT):
        self.m = module
        timeout = timeout_override(module=module, timeout=timeout)
        self.t = httpx.Timeout(timeout=timeout)
        setdefaulttimeout(timeout)
        self.s = self._start()

    def _start(self) -> httpx.Client:
        check_host(module=self.m)
        check_or_load_credentials(module=self.m)
        verify = ssl_verification(module=self.m)
        retries = get_api_retries(module=self.m)
        return httpx.Client(
            base_url=f"https://{self.m.params['firewall']}:{self.m.params['api_port']}/api",
            auth=(self.m.params['api_key'], self.m.params['api_secret']),
            timeout=self.t,
            transport=httpx.HTTPTransport(verify=verify, retries=retries),
        )

    def get(self, cnf: dict) -> dict:
        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

        debug_api(
            module=self.m,
            method='GET',
            url=f'{self.s.base_url}{call_url}',
        )

        try:
            response = check_response(
                module=self.m,
                cnf=cnf,
                response=self.s.get(url=call_url, timeout=self.t)
            )

        except HTTPX_EXCEPTIONS as error:
            raise api_pretty_exception(
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

        debug_api(
            module=self.m,
            method='POST',
            url=f'{self.s.base_url}{call_url}',
            data=data,
            headers=headers,
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
            raise api_pretty_exception(
                method='POST', error=error,
                url=f'{self.s.base_url}{call_url}',
            )

        return response

    def close(self) -> None:
        self.s.close()


def single_get(module: AnsibleModule, cnf: dict, timeout: float = DEFAULT_TIMEOUT) -> dict:
    s = Session(module=module, timeout=timeout)
    response = s.get(cnf=cnf)
    s.close()
    return response


def single_post(module: AnsibleModule, cnf: dict, timeout: float = DEFAULT_TIMEOUT, headers: dict = None) -> dict:
    s = Session(module=module, timeout=timeout)
    response = s.post(cnf=cnf, headers=headers)
    s.close()
    return response
