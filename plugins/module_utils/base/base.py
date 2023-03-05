# could be implemented using inheritance in the future..

# pylint: disable=W0212,R0912

from typing import Callable

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    single_get, single_post
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_simple_existing, to_digit, get_matching, simplify_translate, is_unset


class Base:
    DIFF_FLOAT_ROUND = 1
    RESP_JOIN_CHAR = ','
    ATTR_JOIN_CHAR = 'JOIN_CHAR'
    ATTR_AK = 'API_KEY'  # ak 0-3 used for edge-cases
    ATTR_AK1 = 'API_KEY_1'
    ATTR_AK2 = 'API_KEY_2'
    ATTR_AK3 = 'API_KEY_3'
    ATTR_AK_PATH = 'API_KEY_PATH'
    ATTR_AK_PATH_REQ = 'API_KEY_PATH_REQ'  # if a custom path depth is needed
    ATTR_REQ_NO_AK = 'REQUEST_NO_API_KEY'
    ATTR_AK_PATH_SPLIT_CHAR = '.'
    ATTR_BOOL_INVERT = 'FIELDS_BOOL_INVERT'
    ATTR_TRANSLATE = 'FIELDS_TRANSLATE'
    ATTR_DIFF_EXCL = 'FIELDS_DIFF_EXCLUDE'
    ATTR_VALUE_MAP = 'FIELDS_VALUE_MAPPING'
    ATTR_RELOAD = 'API_CONT_REL'
    ATTR_HEADERS = 'call_headers'
    ATTR_TYPING = 'FIELDS_TYPING'
    ATTR_FIELD_ID = 'FIELD_ID'
    PARAM_MATCH_FIELDS = 'match_fields'

    def __init__(self, instance):
        self.i = instance  # module-specific object
        self.e = {}  # existing entry

        if not hasattr(self.i, self.ATTR_AK) and not hasattr(self.i, self.ATTR_AK_PATH):
            raise ValueError(
                f"Module has neither '{self.ATTR_AK_PATH}' nor "
                f"'{self.ATTR_AK}' attributes set!"
            )

    def search(self, fail_response: bool = False) -> (dict, list):
        if fail_response:
            # find response keys in initial development
            raise SystemExit(self.i.s.get(cnf={
                **self.i.call_cnf, **{'command': self.i.CMDS['search']}
            }))

        AK = {}

        for _ak in [self.ATTR_AK, self.ATTR_AK1, self.ATTR_AK2, self.ATTR_AK3]:
            if hasattr(self.i, _ak):
                AK[_ak] = getattr(self.i, _ak)

        data = self.i.s.get(cnf={
            **self.i.call_cnf, **{'command': self.i.CMDS['search']}
        })

        if hasattr(self.i, self.ATTR_AK_PATH):
            for k in getattr(self.i, self.ATTR_AK_PATH).split(self.ATTR_AK_PATH_SPLIT_CHAR):
                data = data[k]

            if self.ATTR_AK in AK and \
                    isinstance(data, dict):  # if AK_PATH includes AK
                if AK[self.ATTR_AK] in data:
                    data = data[AK[self.ATTR_AK]]

            return data

        if self.ATTR_AK3 in AK:
            return data[AK[self.ATTR_AK1]][AK[self.ATTR_AK2]][AK[self.ATTR_AK3]][AK[self.ATTR_AK]]

        if self.ATTR_AK2 in AK:
            return data[AK[self.ATTR_AK1]][AK[self.ATTR_AK2]][AK[self.ATTR_AK]]

        if self.ATTR_AK1 in AK:
            return data[AK[self.ATTR_AK1]][AK[self.ATTR_AK]]

        return data[AK[self.ATTR_AK]]

    def get_existing(self, diff_filter: bool = False) -> list:
        if diff_filter:
            # use already existing filtering to get 'clean' int/.. values
            return get_simple_existing(
                entries=self._call_search(),
                simplify_func=self._call_simple(),
                add_filter=self.build_diff,
            )

        return get_simple_existing(
            entries=self._call_search(),
            simplify_func=self._call_simple(),
        )

    def find(self, match_fields: list) -> None:
        if self.i.existing_entries is None:
            self.i.existing_entries = self._call_search()

        match = get_matching(
            module=self.i.m, existing_items=self.i.existing_entries,
            compare_item=self.i.p, match_fields=match_fields,
            simplify_func=self._call_simple(),
        )

        if match is not None:
            setattr(self.i, self.i.EXIST_ATTR, match)
            self.i.exists = True
            self.i.r['diff']['before'] = self.build_diff(data=match)

            if 'uuid' in match:
                self.i.call_cnf['params'] = [match['uuid']]

    def process(self) -> None:
        if 'state' in self.i.p and self.i.p['state'] == 'absent':
            if self.i.exists:
                if hasattr(self.i, 'delete'):
                    self.i.delete()

                else:
                    self.delete()

        else:
            if 'state' not in self.i.p or self.i.exists:
                if hasattr(self.i, 'update'):
                    self.i.update()

                else:
                    self.update()

            else:
                if hasattr(self.i, 'create'):
                    self.i.create()

                else:
                    self.create()

    def create(self) -> dict:
        self.i.r['changed'] = True

        if not self.i.m.check_mode:
            return self.i.s.post(cnf={
                **self.i.call_cnf, **{
                    'command': self.i.CMDS['add'],
                    'data': self._get_request_data(),
                }
            })

    def update(self, enable_switch: bool = True) -> dict:
        self._set_existing()

        # checking if changed
        for field in self.i.FIELDS_CHANGE:
            if field in self.i.p:
                if self.PARAM_MATCH_FIELDS in self.i.p:
                    if field in self.i.p[self.PARAM_MATCH_FIELDS]:
                        continue

                if hasattr(self.i, self.ATTR_FIELD_ID):
                    if field == getattr(self.i, self.ATTR_FIELD_ID):
                        continue

                if str(self.e[field]) != str(self.i.p[field]):
                    self.i.r['changed'] = True

                    if self.i.p['debug']:
                        self.i.m.warn(
                            f"Field changed: '{field}' "
                            f"'{self.e[field]}' != '{self.i.p[field]}'"
                        )

                    break

        # update if changed
        if self.i.r['changed']:
            if self.i.p['debug']:
                self.i.m.warn(f"{self.i.r['diff']}")

            if not self.i.m.check_mode:
                if hasattr(self.i, '_update_call'):
                    response = self.i._update_call()

                else:
                    response = self._api_post(cnf={
                        **self.i.call_cnf, **{
                            'command': self.i.CMDS['set'],
                            'data': self._get_request_data(),
                        }
                    })

                if self.i.p['debug']:
                    self.i.m.warn(f"{self.i.r['diff']}")

                return response

        elif enable_switch:
            self._update_enabled()

    def _update_enabled(self) -> None:
        existing = getattr(self.i, self.i.EXIST_ATTR)

        if 'enabled' in existing:
            if existing['enabled'] != self.i.p['enabled']:
                BOOL_INVERT_FIELDS = []
                enable = self.i.p['enabled']
                invert = False

                if hasattr(self.i, self.ATTR_BOOL_INVERT):
                    BOOL_INVERT_FIELDS = getattr(self.i, self.ATTR_BOOL_INVERT)

                if 'enabled' in BOOL_INVERT_FIELDS:
                    invert = True
                    enable = not enable

                if enable:
                    if hasattr(self.i, 'enable'):
                        self.i.enable()

                    else:
                        self.enable(invert=invert)

                else:
                    if hasattr(self.i, 'disable'):
                        self.i.disable()

                    else:
                        self.disable(invert=invert)

    def delete(self) -> dict:
        self.i.r['changed'] = True
        self.i.r['diff']['after'] = {}

        if not self.i.m.check_mode:
            if hasattr(self.i, '_delete_call'):
                response = self.i._delete_call()

            else:
                response = self._api_post(cnf={
                    **self.i.call_cnf,
                    **{'command': self.i.CMDS['del']}
                })

            if self.i.p['debug']:
                self.i.m.warn(f"{self.i.r['diff']}")

            return response

    def reload(self) -> dict:
        # reload the running config
        if hasattr(self.i, self.ATTR_RELOAD):
            cont_rel = getattr(self.i, self.ATTR_RELOAD)

        else:
            cont_rel = self.i.API_CONT

        if not self.i.m.check_mode:
            return self.i.s.post(cnf={
                'module': self.i.API_MOD,
                'controller': cont_rel,
                'command': self.i.API_CMD_REL,
                'params': []
            })

    def _get_request_data(self) -> dict:
        if hasattr(self.i, '_build_request'):
            return self.i._build_request()

        return self.build_request()

    def _change_enabled_state(self, value: int) -> dict:
        return self._api_post(cnf={
            **self.i.call_cnf, **{
                'command': self.i.CMDS['toggle'],
                'params': [getattr(self.i, self.i.EXIST_ATTR)['uuid'], value],
            }
        })

    def _is_enabled(self, invert: bool) -> bool:
        is_enabled = getattr(self.i, self.i.EXIST_ATTR)['enabled']

        if invert:
            is_enabled = not is_enabled

        return is_enabled

    def enable(self, invert: bool = False) -> dict:
        if self.i.exists and not self._is_enabled(invert=invert):
            self.i.r['changed'] = True
            self.i.r['diff']['before'] = {'enabled': False}
            self.i.r['diff']['after'] = {'enabled': True}

            if not self.i.m.check_mode:
                return self._change_enabled_state(1)

    def disable(self, invert: bool = False) -> dict:
        if self.i.exists and self._is_enabled(invert=invert):
            self.i.r['changed'] = True
            self.i.r['diff']['before'] = {'enabled': True}
            self.i.r['diff']['after'] = {'enabled': False}

            if not self.i.m.check_mode:
                return self._change_enabled_state(0)

    def build_diff(self, data: dict) -> dict:
        if not isinstance(data, dict):
            raise ValueError('The diff-source object must be of type dict!')

        EXCLUDE_FIELDS = []

        if hasattr(self.i, self.ATTR_DIFF_EXCL):
            EXCLUDE_FIELDS = getattr(self.i, self.ATTR_DIFF_EXCL)

        self._set_existing()

        diff = {
            'uuid': self.e['uuid'] if 'uuid' in self.e else None
        }

        for field in self.i.FIELDS_ALL:
            if field in EXCLUDE_FIELDS:
                continue

            stringify = True

            try:
                diff[field] = data[field]

            except KeyError:
                if field in self.i.p:
                    diff[field] = self.i.p[field]

            if isinstance(diff[field], list):
                diff[field].sort()
                stringify = False

            elif isinstance(diff[field], str) and diff[field].isnumeric:
                try:
                    diff[field] = int(diff[field])
                    stringify = False

                except (TypeError, ValueError):
                    pass

            elif isinstance(diff[field], dict) and 'uuid' in diff[field]:
                diff[field] = diff[field]['uuid']

            elif isinstance(diff[field], (bool, int)):
                stringify = False

            if stringify:
                try:
                    diff[field] = round(float(diff[field]), self.DIFF_FLOAT_ROUND)
                    stringify = False

                except (TypeError, ValueError):
                    pass

            if stringify:
                diff[field] = str(diff[field])

        return diff

    def build_request(self, ignore_fields: list = None) -> dict:
        request = {}
        TRANSLATE_FIELDS = {}
        BOOL_INVERT_FIELDS = []

        if ignore_fields is None:
            ignore_fields = []

        if is_unset(self.e):
            self.e = getattr(self.i, self.i.EXIST_ATTR)

        if hasattr(self.i, self.ATTR_TRANSLATE):
            TRANSLATE_FIELDS = getattr(self.i, self.ATTR_TRANSLATE)

        if hasattr(self.i, self.ATTR_BOOL_INVERT):
            BOOL_INVERT_FIELDS = getattr(self.i, self.ATTR_BOOL_INVERT)

        for field in self.i.FIELDS_ALL:
            if field in ignore_fields:
                continue

            opn_field = field
            if field in TRANSLATE_FIELDS:
                opn_field = TRANSLATE_FIELDS[field]

            if field in self.i.p:
                opn_data = self.i.p[field]

            else:
                opn_data = self.e[field]

            if isinstance(opn_data, bool):
                if field in BOOL_INVERT_FIELDS:
                    opn_data = not opn_data

                request[opn_field] = to_digit(opn_data)

            elif isinstance(opn_data, list):
                join_char = self.RESP_JOIN_CHAR

                if hasattr(self.i, self.ATTR_JOIN_CHAR):
                    join_char = getattr(self.i, self.ATTR_JOIN_CHAR)

                request[opn_field] = join_char.join(opn_data)

            else:
                request[opn_field] = opn_data

        payload = request

        if not hasattr(self.i, self.ATTR_REQ_NO_AK):
            if hasattr(self.i, self.ATTR_AK):
                payload = {getattr(self.i, self.ATTR_AK): payload}

            elif hasattr(self.i, self.ATTR_AK_PATH_REQ):
                ak_path = getattr(self.i, self.ATTR_AK_PATH_REQ).split(self.ATTR_AK_PATH_SPLIT_CHAR)
                ak_path.reverse()

                for k in ak_path:
                    payload = {k: payload}

            elif hasattr(self.i, self.ATTR_AK_PATH):
                # request only needs the last key
                attr_ak = getattr(self.i, self.ATTR_AK_PATH).rsplit(self.ATTR_AK_PATH_SPLIT_CHAR, 1)[1]
                payload = {attr_ak: payload}

        return payload

    def _set_existing(self) -> None:
        if is_unset(self.e):
            _existing = getattr(self.i, self.i.EXIST_ATTR)

            if _existing is not None and len(_existing) > 0:
                self.e = _existing

    def _simplify_existing(self, existing: dict) -> dict:
        translate, typing, bool_invert, value_map = {}, {}, [], {}

        if hasattr(self.i, self.ATTR_TRANSLATE):
            translate = getattr(self.i, self.ATTR_TRANSLATE)

        if hasattr(self.i, self.ATTR_TYPING):
            typing = getattr(self.i, self.ATTR_TYPING)

        if hasattr(self.i, self.ATTR_BOOL_INVERT):
            bool_invert = getattr(self.i, self.ATTR_BOOL_INVERT)

        if hasattr(self.i, self.ATTR_VALUE_MAP):
            value_map = getattr(self.i, self.ATTR_VALUE_MAP)

        return simplify_translate(
            existing=existing,
            typing=typing,
            translate=translate,
            bool_invert=bool_invert,
            value_map=value_map,
        )

    def _call_simple(self) -> Callable:
        if hasattr(self.i, 'simplify_existing'):
            return self.i.simplify_existing

        if hasattr(self.i, '_simplify_existing'):
            return self.i._simplify_existing

        return self._simplify_existing

    def _call_search(self) -> (list, dict):
        if hasattr(self.i, '_search_call'):
            return self.i._search_call()

        if hasattr(self.i, 'search_call'):
            return self.i.search_call()

        return self.search()

    def _api_headers(self) -> dict:
        if hasattr(self.i, self.ATTR_HEADERS):
            return getattr(self.i, self.ATTR_HEADERS)

        return {}

    def _api_post(self, cnf: dict) -> (dict, list):
        if hasattr(self.i, 's'):
            return self.i.s.post(
                cnf=cnf,
                headers=self._api_headers()
            )

        return single_post(
            cnf=cnf,
            module=self.i.m,
            headers=self._api_headers()
        )

    def _api_get(self, cnf: dict) -> (dict, list):
        if hasattr(self.i, 's'):
            return self.i.s.get(cnf=cnf)

        return single_get(
            cnf=cnf,
            module=self.i.m
        )
