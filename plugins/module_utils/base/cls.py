from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, validate_str_fields


class BaseModule:
    def __init__(self, m: AnsibleModule, r: dict, s: Session = None):
        if hasattr(self, 'TIMEOUT'):
            self.s = Session(
                module=m,
                timeout=self.TIMEOUT,
            ) if s is None else s

        else:
            self.s = Session(module=m) if s is None else s

        self.m = m
        self.p = m.params
        self.r = r
        self.b = Base(instance=self)
        self.exists = False
        self.existing_entries = None
        self.call_cnf = {
            'module': self.b.i.API_MOD,
            'controller': self.b.i.API_CONT,
        }

    def _search_call(self, fail_response: bool = False) -> list:
        return self.b.search(fail_response=fail_response)

    def get_existing(self) -> list:
        return self.b.get_existing()

    def process(self) -> None:
        self.b.process()

    def create(self) -> None:
        self.b.create()

    def update(self) -> None:
        self.b.update()

    def delete(self) -> None:
        self.b.delete()

    def reload(self) -> None:
        self.b.reload()


class GeneralModule:
    # has only a single entry; cannot be deleted or created
    EXIST_ATTR = 'settings'

    def __init__(self, m: AnsibleModule, r: dict, s: Session = None):
        if hasattr(self, 'TIMEOUT'):
            self.s = Session(
                module=m,
                timeout=self.TIMEOUT,
            ) if s is None else s

        else:
            self.s = Session(module=m) if s is None else s

        self.m = m
        self.p = m.params
        self.r = r
        self.b = Base(instance=self)
        self.exists = False
        self.existing_entries = None
        self.call_cnf = {
            'module': self.b.i.API_MOD,
            'controller': self.b.i.API_CONT,
        }
        self.settings = {}

    def check(self) -> None:
        if hasattr(self.b.i, 'STR_VALIDATIONS'):
            if hasattr(self.b.i, 'STR_LEN_VALIDATIONS'):
                validate_str_fields(
                    module=self.m,
                    data=self.p,
                    field_regex=self.b.i.STR_VALIDATIONS,
                    field_minmax_length=self.b.i.STR_LEN_VALIDATIONS
                )

            else:
                validate_str_fields(module=self.m, data=self.p, field_regex=self.b.i.STR_VALIDATIONS)

        if hasattr(self.b.i, 'INT_VALIDATIONS'):
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.b.i.INT_VALIDATIONS)

        self.settings = self._search_call()
        self._build_diff()

    def _search_call(self, fail_response: bool = False) -> dict:
        # pylint: disable=W0212
        return self.b._simplify_existing(
            self.b.search(
                fail_response=fail_response
            )
        )

    def get_existing(self) -> dict:
        return self._search_call()

    def process(self) -> None:
        self.update()

    def update(self) -> None:
        self.b.update(enable_switch=False)

    def reload(self) -> None:
        self.b.reload()

    def _build_diff(self) -> None:
        self.r['diff']['before'] = self.b.build_diff(self.settings)
        self.r['diff']['after'] = self.b.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })

    def _build_request(self) -> dict:
        if hasattr(self.b.i, self.b.ATTR_AK3):
            return {self.b.i.API_KEY_1: {self.b.i.API_KEY_2: {self.b.i.API_KEY_3: self.b.build_request()}}}

        if hasattr(self.b.i, self.b.ATTR_AK2):
            return {self.b.i.API_KEY_1: {self.b.i.API_KEY_2: self.b.build_request()}}

        if hasattr(self.b.i, self.b.ATTR_AK1):
            return {self.b.i.API_KEY_1: self.b.build_request()}

        return self.b.build_request()
