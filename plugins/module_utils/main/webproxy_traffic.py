from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    simplify_translate
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Traffic(BaseModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_1 = 'proxy'
    API_KEY_2 = 'general'
    API_KEY = 'traffic'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'download_kb_max', 'upload_kb_max', 'throttle_kb_bandwidth',
        'throttle_kb_host_bandwidth', 'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'download_kb_max': 'maxDownloadSize',
        'upload_kb_max': 'maxUploadSize',
        'throttle_kb_bandwidth': 'OverallBandwidthTrotteling',
        'throttle_kb_host_bandwidth': 'perHostTrotteling',
    }
    FIELDS_TYPING = {
        'int': [
            'download_kb_max', 'upload_kb_max', 'throttle_kb_bandwidth',
            'throttle_kb_host_bandwidth',
        ],
        'bool': ['enabled']
    }
    EXIST_ATTR = 'settings'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.settings = {}
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.s = Session(
            module=module,
            timeout=self.TIMEOUT,
        ) if session is None else session

    def check(self):
        self.settings = self._search_call()
        self.r['diff']['before'] = self.b.build_diff(self.settings)
        self.r['diff']['after'] = self.b.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })

    def _search_call(self) -> dict:
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1][self.API_KEY_2][self.API_KEY]

        return simplify_translate(
            existing=settings,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
        )

    def get_existing(self) -> dict:
        return self._search_call()

    def _build_request(self) -> dict:
        return {self.API_KEY_1: {self.API_KEY_2: self.b.build_request()}}

    def update(self):
        self.b.update(enable_switch=False)
