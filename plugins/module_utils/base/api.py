from json import dumps as json_dumps
from json import loads as json_loads
from os import environ, unlink
from shutil import which
from socket import setdefaulttimeout
from subprocess import PIPE, run as subprocess_run
from tempfile import NamedTemporaryFile

import httpx

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import \
    check_host, ssl_verification, check_response, get_params_path, debug_api, \
    check_or_load_credentials, api_pretty_exception
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import is_ip6

DEFAULT_TIMEOUT = 20.0
HTTPX_EXCEPTIONS = (
    httpx.ConnectTimeout, httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout,
    httpx.TimeoutException, httpx.PoolTimeout, httpx.RemoteProtocolError,
)
# Strict HTTP parsers (httpx/h11, urllib) can fail on large OPNsense chunked
# responses with "illegal chunk header" / "malformed chunk footer" /
# IncompleteRead, while curl reads the same payload successfully.
PROTOCOL_ERROR_MARKERS = (
    'illegal chunk header',
    'malformed chunk footer',
    'IncompleteRead',
    'RemoteProtocolError',
)


class _CurlResponse:
    """Minimal response object compatible with check_response()."""

    def __init__(self, status_code: int, content: bytes, url: str):
        self.status_code = status_code
        self.content = content
        self.text = content.decode('utf-8', errors='replace')
        self.url = url
        self.headers = {}
        self.is_closed = True
        self.is_stream_consumed = True

    def json(self):
        return json_loads(self.content)


class Session:
    def __init__(self, module: AnsibleModule, timeout: float = DEFAULT_TIMEOUT):
        self.m = module
        self.timeout = timeout
        self.api_key = None
        self.api_secret = None
        self.ssl_verify = True
        self.ssl_ca_file = None
        self.proxy = None
        self.base_url = ''
        self.s = self._start(timeout)

    def _start(self, timeout: float) -> httpx.Client:
        check_host(module=self.m)
        api_key, api_secret = check_or_load_credentials(module=self.m)
        if api_secret is None:
            api_key = self.m.params['api_key']
            api_secret = self.m.params['api_secret']

        self.api_key = api_key
        self.api_secret = api_secret

        if 'api_timeout' in self.m.params and self.m.params['api_timeout'] is not None:
            timeout = self.m.params['api_timeout']
            self.timeout = timeout

        setdefaulttimeout(timeout)

        fw = self.m.params['firewall']
        if is_ip6(fw, strip_enclosure=False):
            fw = f"[{fw}]"

        proxy = environ.get('HTTPS_PROXY', None)
        if proxy is not None and not proxy.startswith('http') and not proxy.startswith('sock'):
            proxy = None
        self.proxy = proxy

        self.ssl_verify = bool(self.m.params.get('ssl_verify', True))
        self.ssl_ca_file = self.m.params.get('ssl_ca_file')
        self.base_url = f"https://{fw}:{self.m.params['api_port']}/api"

        return httpx.Client(
            base_url=self.base_url,
            auth=(api_key, api_secret),
            timeout=httpx.Timeout(timeout=timeout, connect=2.0),
            transport=httpx.HTTPTransport(
                verify=ssl_verification(module=self.m),
                retries=self.m.params['api_retries'],
                proxy=proxy,
            ),
            # Prefer identity encoding so proxies/servers are less likely to emit
            # broken gzip+chunked payloads that strict parsers reject.
            headers={
                'User-Agent': 'Ansible',
                'Accept-Encoding': 'identity',
            },
        )

    @staticmethod
    def _is_protocol_parse_error(error) -> bool:
        message = str(error)
        return any(marker in message for marker in PROTOCOL_ERROR_MARKERS)

    def _curl_request(self, method: str, call_url: str, data: dict = None, headers: dict = None) -> _CurlResponse:
        if which('curl') is None:
            raise RuntimeError('curl is required to retry after an HTTP protocol parse error')

        url = f"{self.base_url}/{call_url.lstrip('/')}"
        argv = [
            'curl',
            '--silent',
            '--show-error',
            '--max-time', str(int(self.timeout) if self.timeout else int(DEFAULT_TIMEOUT)),
            '--user', f'{self.api_key}:{self.api_secret}',
            '--request', method.upper(),
            '--header', 'Accept-Encoding: identity',
            '--header', 'User-Agent: Ansible',
            '--write-out', '\n%{http_code}',
        ]

        if not self.ssl_verify:
            argv.append('--insecure')
        elif self.ssl_ca_file:
            argv.extend(['--cacert', self.ssl_ca_file])

        if self.proxy:
            argv.extend(['--proxy', self.proxy])

        if headers:
            for key, value in headers.items():
                argv.extend(['--header', f'{key}: {value}'])

        tmp_path = None
        try:
            if data is not None:
                with NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as tmp:
                    tmp.write(json_dumps(data))
                    tmp_path = tmp.name
                argv.extend(['--header', 'Content-Type: application/json', '--data-binary', f'@{tmp_path}'])

            argv.append(url)
            completed = subprocess_run(
                argv,
                stdout=PIPE,
                stderr=PIPE,
                check=False,
            )
        finally:
            if tmp_path is not None:
                try:
                    unlink(tmp_path)
                except OSError:
                    pass

        if completed.returncode != 0:
            stderr = completed.stderr.decode('utf-8', errors='replace').strip()
            raise RuntimeError(f'curl failed ({completed.returncode}): {stderr}')

        raw = completed.stdout
        # Trailing "\n{status}" added by --write-out
        try:
            body, status_bytes = raw.rsplit(b'\n', 1)
            status_code = int(status_bytes.decode('ascii'))
        except (ValueError, AttributeError) as error:
            raise RuntimeError(f'Unable to parse curl status code from response: {error}') from error

        return _CurlResponse(status_code=status_code, content=body, url=url)

    def _request(self, method: str, cnf: dict, data: dict = None, headers: dict = None):
        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"
        full_url = f'{self.base_url}/{call_url}'

        debug_api(
            module=self.m,
            method=method.upper(),
            url=full_url,
            data=data,
            headers=headers,
        )

        try:
            if method.upper() == 'GET':
                response = self.s.get(url=call_url)
            else:
                response = self.s.post(url=call_url, json=data, headers=headers or {})
            return check_response(module=self.m, cnf=cnf, response=response)

        except HTTPX_EXCEPTIONS as error:
            if not self._is_protocol_parse_error(error):
                api_pretty_exception(
                    m=self.m, method=method.upper(), error=error,
                    url=full_url,
                )
                raise

            try:
                # Truncate: httpx may embed large response fragments in the error.
                error_summary = str(error)
                if len(error_summary) > 160:
                    error_summary = error_summary[:157] + '...'
                self.m.warn(
                    f"httpx failed to parse OPNsense response for '{method.upper()} => {full_url}' "
                    f"({error_summary}); retrying with curl"
                )
                response = self._curl_request(
                    method=method,
                    call_url=call_url,
                    data=data,
                    headers=headers,
                )
                return check_response(module=self.m, cnf=cnf, response=response)

            except Exception as curl_error:
                api_pretty_exception(
                    m=self.m, method=method.upper(), error=curl_error,
                    url=full_url,
                )
                raise

    def get(self, cnf: dict) -> dict:
        return self._request(method='GET', cnf=cnf)

    def post(self, cnf: dict, headers: dict = None) -> dict:
        if headers is None:
            headers = {}

        data = None

        if 'data' in cnf and cnf['data'] is not None and len(cnf['data']) > 0:
            headers = dict(headers)
            headers['Content-Type'] = 'application/json'
            data = cnf['data']

        return self._request(method='POST', cnf=cnf, data=data, headers=headers)

    def close(self) -> None:
        self.s.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def single_get(module: AnsibleModule, cnf: dict, timeout: float = DEFAULT_TIMEOUT) -> dict:
    with Session(module=module, timeout=timeout) as s:
        response = s.get(cnf=cnf)

    return response


def single_post(module: AnsibleModule, cnf: dict, timeout: float = DEFAULT_TIMEOUT, headers: dict = None) -> dict:
    with Session(module=module, timeout=timeout) as s:
        response = s.post(cnf=cnf, headers=headers)

    return response
