from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, DUMMY_MODULE
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.util_pytest import log_test
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.base_testdata import \
    MockOPNsenseController, GenericTestdata


def test_session_creation():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
    s = Session(module=DUMMY_MODULE)
    s.close()


def test_httpx_protocol_error_retries_with_curl(mocker):
    """Large OPNsense chunked responses can fail in httpx/h11; curl should retry."""
    import httpx
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import (
        Session,
        _CurlResponse,
    )

    pytest_mock_http_responses(mocker=mocker, handler=Testdata())

    with Session(module=DUMMY_MODULE) as s:
        mocker.patch.object(
            s.s,
            'get',
            side_effect=httpx.RemoteProtocolError('illegal chunk header: bytearray(b\'x\')'),
        )
        mocker.patch.object(
            s,
            '_curl_request',
            return_value=_CurlResponse(
                status_code=200,
                content=b'{"alias":{"aliases":{"alias":{}}}}',
                url='https://example/api/firewall/alias/get',
            ),
        )
        res = s.get({'module': 'firewall', 'controller': 'alias', 'command': 'get'})
        assert res == {'alias': {'aliases': {'alias': {}}}}



def test_session_contextmanager():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
    with Session(module=DUMMY_MODULE):
        pass


class Testdata(MockOPNsenseController):
    def commands(self) -> dict:
        return {
            'get': self._get,
            'set': self._set,
        }


def test_requests(mocker):
    log_test('api-requests')

    cnf = {'module': 'module', 'controller': 'controller'}

    pytest_mock_http_responses(
        mocker=mocker,
        handler=Testdata()
    )

    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session, single_get, single_post
    with Session(module=DUMMY_MODULE) as s:
        res = s.get({**cnf, 'command': 'get'})
        assert len(res) == 0

        res = s.post({**cnf, 'command': 'set'})
        assert res == MockOPNsenseController.RES_ERROR

    assert single_get(module=DUMMY_MODULE, cnf={**cnf, 'command': 'get'}) == {}
    assert single_post(module=DUMMY_MODULE, cnf={**cnf, 'command': 'set'}) == MockOPNsenseController.RES_ERROR


def test_check_testdata(mocker):
    log_test('api-check-testdata')

    cnf = {'module': 'module', 'controller': 'controller'}

    testdata = GenericTestdata()
    pytest_mock_http_responses(
        mocker=mocker,
        handler=testdata,
    )

    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session, single_get, single_post
    with Session(module=DUMMY_MODULE) as s:
        res_empty = {'test': {'tests': {'test': {}}}}

        # no entries exist
        res = s.get({**cnf, 'command': 'get'})
        assert res == res_empty
        assert res == testdata.pack_data({})

        res = s.post({**cnf, 'command': 'set_test'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': '<uuid>'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': '<uuid>', 'data': {'test': 'x'}})
        assert res == MockOPNsenseController.RES_ERROR

        res = s.post({**cnf, 'command': 'del_test'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'del_test', 'params': '<uuid>'})
        assert res == MockOPNsenseController.RES_ERROR

        # create entry
        res = s.post({**cnf, 'command': 'add_test', 'data': {'p1': 'a'}})
        assert res == MockOPNsenseController.RES_SUCCESS

        # list should contain new entry in {'<uuid>': '<entry>'} format
        res = s.get({**cnf, 'command': 'get'})
        entries = testdata.unpack_data(res)
        assert len(entries) == 1
        entry_key = list(entries.keys())[0]

        assert res == {'test': {'tests': {'test': {
            entry_key: {'p1': 'a'},
        }}}}
        assert list(entries.values()) == [{'p1': 'a'}]

        # update entry
        res = s.post({**cnf, 'command': 'set_test'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': '<uuid>'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': '<uuid>', 'data': {'p1': 'x'}})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': entry_key, 'data': {'p1': 'aa'}})
        assert res == MockOPNsenseController.RES_SUCCESS

        # checking that entry was updated
        res = s.get({**cnf, 'command': 'get'})
        entries = testdata.unpack_data(res)
        assert len(entries) == 1
        assert entries[entry_key] == {'p1': 'aa'}

        # deleting entry
        res = s.post({**cnf, 'command': 'del_test'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'del_test', 'params': '<uuid>'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'del_test', 'params': entry_key})
        assert res == MockOPNsenseController.RES_SUCCESS

        # checking that the entry was deleted
        res = s.get({**cnf, 'command': 'get'})
        assert res == res_empty
