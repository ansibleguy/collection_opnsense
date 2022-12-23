from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, simplify_translate
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Cache(BaseModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_1 = 'proxy'
    API_KEY_2 = 'general'
    API_KEY_3 = 'cache'
    API_KEY = 'local'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'memory_mb', 'size_mb', 'directory', 'layer_1', 'layer_2',
        'size_mb_max', 'memory_kb_max', 'memory_cache_mode',
        'cache_linux_packages', 'cache_windows_updates',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'memory_mb': 'cache_mem',
        'size_mb': 'size',
        'size_mb_max': 'maximum_object_size',
        'memory_kb_max': 'maximum_object_size_in_memory',
        'layer_1': 'l1',
        'layer_2': 'l2',
    }
    FIELDS_TYPING = {
        'bool': ['cache_linux_packages', 'cache_windows_updates'],
        'select': ['memory_cache_mode'],
        'int': [
            'memory_mb', 'size_mb', 'layer_1', 'layer_2', 'size_mb_max',
            'memory_kb_max'
        ],
    }
    INT_VALIDATIONS = {
        'size_mb_max': {'min': 1, 'max': 99999},
        'memory_kb_max': {'min': 1, 'max': 99999},
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
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.settings = self._search_call()
        self.r['diff']['before'] = self.b.build_diff(self.settings)
        self.r['diff']['after'] = self.b.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })

    def _search_call(self) -> dict:
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1][self.API_KEY_2][self.API_KEY_3][self.API_KEY]

        return simplify_translate(
            existing=settings,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
        )

    def get_existing(self) -> dict:
        return self._search_call()

    def _build_request(self) -> dict:
        return {self.API_KEY_1: {self.API_KEY_2: {self.API_KEY_3: self.b.build_request()}}}

    def update(self):
        self.b.update(enable_switch=False)
