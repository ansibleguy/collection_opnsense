# pylint: disable=C0415


class AnsibleError(Exception):
    pass


class DummyModule:
    def __init__(self):
        self.params = dict(
            firewall='127.0.0.1',
            api_port=51337,
            api_key='dummy',
            api_secret='secret',
            api_credential_file=None,
            ssl_verify=False,
            ssl_ca_file=None,
            debug=False,
            profiling=False,
            api_timeout=None,
            api_retries=0,
        )

    def fail_json(self, msg: str):
        raise AnsibleError(msg)


DUMMY_MODULE = DummyModule()
DUMMY_REQ = dict(
    module='dummy',
    controller='dummy',
    command='test',
)


def test_session_creation():
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
    s = Session(module=DUMMY_MODULE)
    s.close()


# todo: to test this we need to create a http-server that's able to abort connections before they are established
# @pytest.mark.parametrize('retries', [
#     0,
#     1,
# ])
# def test_retries(retries: int):
#     from http.server import HTTPServer, BaseHTTPRequestHandler
#     from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
#
#     class WebRequestHandler(BaseHTTPRequestHandler):
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.count = 0
#             self.ok_count = retries
#
#         def do_GET(self):
#             if self.count == self.ok_count:
#                 self.send_response(200)
#
#             else:
#                 self.send_response(400)
#
#             self.count += 1
#             self.end_headers()
#             sleep(1)
#             self.wfile.write('done'.encode('utf-8'))
#
#     with HTTPServer((DUMMY_MODULE.params['firewall'], DUMMY_MODULE.params['api_port']), WebRequestHandler):
#         DUMMY_MODULE.params['retries'] = retries
#         Session(module=DUMMY_MODULE).s.get(
#             url=f"http://{DUMMY_MODULE.params['firewall']}:{DUMMY_MODULE.params['api_port']}",
#         )
