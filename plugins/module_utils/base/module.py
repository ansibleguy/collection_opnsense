from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.logic import BaseLogic


class BaseModule(BaseLogic):
    def __init__(self, m: AnsibleModule, r: dict, s: Session = None, f: dict = None, multi: dict = None):
        super().__init__(m, r, s)
        if f is None:
            f = {}

        if multi is not None and len(multi) > 0:
            # override params by MultiModule
            self.p = multi

        self.fail_verify = f.get('verify', False)
        self.fail_process = f.get('process', False)

    def _base_check(self, match_fields: list = None):
        self._check_validators()

        if match_fields is None:
            if 'match_fields' in self.p:
                match_fields = self.p['match_fields']

            elif hasattr(self, 'FIELD_ID'):
                match_fields = [self.FIELD_ID]

        if match_fields is not None:
            self.find(match_fields=match_fields)
            if self.exists:
                self.call_cnf['params'] = [getattr(self, self.EXIST_ATTR)[self.field_pk]]

        if 'state' not in self.p or self.p['state'] == 'present':
            self.r['diff']['after'] = self.build_diff(data=self.p)

    def check(self) -> None:
        self._base_check()


class GeneralModule(BaseLogic):
    # has only a single entry; cannot be deleted or created
    EXIST_ATTR = 'settings'

    def __init__(self, m: AnsibleModule, r: dict, s: Session = None):
        super().__init__(m, r, s)
        self.settings = {}

    def _base_check(self):
        self._check_validators()
        self.settings = self.search_call()
        self._build_diff()

    def check(self) -> None:
        self._base_check()

    def search_call(self) -> dict:
        return self.simplify_existing(self.search())

    def get_existing(self) -> dict:
        return self.search_call()

    def process(self) -> None:
        self._base_update()

    def update(self) -> None:
        self._base_update(enable_switch=False)

    def _build_diff(self) -> None:
        self.r['diff']['before'] = self.build_diff(self.settings)
        self.r['diff']['after'] = self.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })
