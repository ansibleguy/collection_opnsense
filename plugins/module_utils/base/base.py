# could be implemented using inheritance in the future..

# NOTE: pylint is basically right, but I really do not want to take the time to refactor this..
# pylint: disable=W0212,R0912,R0915

from typing import Callable

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    single_get, single_post
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_simple_existing, to_digit, get_matching, simplify_translate, is_unset, \
    sort_param_lists
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    exit_bug, exit_debug, ModuleSoftError


class Base:
    DIFF_FLOAT_ROUND = 1
    RESP_JOIN_CHAR = ','
    ATTR_JOIN_CHAR = 'JOIN_CHAR'
    ATTR_AK_PATH = 'API_KEY_PATH'
    ATTR_AK_PATH_REQ = 'API_KEY_PATH_REQ'  # if a custom path depth is needed
    ATTR_AK_PATH_GET = 'API_KEY_PATH_GET'  # if 'get' needs custom path
    ATTR_GET_ADD = 'SEARCH_ADDITIONAL'  # extract additional data from search-call
    ATTR_AK_PATH_SPLIT_CHAR = '.'
    ATTR_BOOL_INVERT = 'FIELDS_BOOL_INVERT'
    ATTR_TRANSLATE = 'FIELDS_TRANSLATE'
    ATTR_DIFF_EXCL = 'FIELDS_DIFF_EXCLUDE'
    ATTR_VALUE_MAP = 'FIELDS_VALUE_MAPPING'
    ATTR_VALUE_MAP_RCV = 'FIELDS_VALUE_MAPPING_RCV'
    ATTR_FIELD_ALL = 'FIELDS_ALL'
    ATTR_FIELD_CH = 'FIELDS_CHANGE'
    ATTR_REL_CONT = 'API_CONT_REL'
    ATTR_GET_CONT = 'API_CONT_GET'
    ATTR_GET_MOD = 'API_MOD_GET'
    ATTR_API_MOD = 'API_MOD'
    ATTR_API_CONT = 'API_CONT'
    ATTR_HEADERS = 'call_headers'
    ATTR_TYPING = 'FIELDS_TYPING'
    ATTR_FIELD_ID = 'FIELD_ID'
    PARAM_MATCH_FIELDS = 'match_fields'

    REQUIRED_ATTRS = [
        ATTR_AK_PATH,
        ATTR_TYPING,
        ATTR_API_MOD,
        ATTR_API_CONT,
        ATTR_FIELD_ALL,
        ATTR_FIELD_CH,
    ]

    def __init__(self, instance):
        self.i = instance  # module-specific object
        self.e = {}  # existing entry

        for attr in self.REQUIRED_ATTRS:
            if not hasattr(self.i, attr):
                exit_bug(f"Module has no '{attr}' attribute set!")

    def search(self, fail_response: bool = False) -> (dict, list):
        if fail_response:
            # find response keys in initial development
            exit_debug(self.i.s.get(cnf={
                **self.i.call_cnf, **{'command': self.i.CMDS['search']}
            }))

        # workaround if 'get' needs to be performed using other api module/controller
        cont_get, mod_get = self.i.API_CONT, self.i.API_MOD

        if hasattr(self.i, self.ATTR_GET_CONT):
            cont_get = getattr(self.i, self.ATTR_GET_CONT)

        if hasattr(self.i, self.ATTR_GET_MOD):
            mod_get = getattr(self.i, self.ATTR_GET_MOD)

        data = self.i.s.get(cnf={
            **self.i.call_cnf,
            **{
                'module': mod_get,
                'controller': cont_get,
                'command': self.i.CMDS['search'],
            }
        })

        if hasattr(self.i, self.ATTR_GET_ADD):
            for attr, ak_path in getattr(self.i, self.ATTR_GET_ADD).items():
                if hasattr(self.i, attr):
                    setattr(
                        self.i, attr,
                        self._search_path_handling(data=data, ak_path=ak_path)
                    )

        return self._search_path_handling(data)

    def _search_path_handling(self, data: dict, ak_path: str = None) -> dict:
        # resolving API_KEY_PATH's so data from nested dicts gets extracted as configured
        if ak_path is None:
            if hasattr(self.i, self.ATTR_AK_PATH_GET):
                ak_path = getattr(self.i, self.ATTR_AK_PATH_GET)

            elif hasattr(self.i, self.ATTR_AK_PATH):
                ak_path = getattr(self.i, self.ATTR_AK_PATH)

        if ak_path is not None:
            for k in ak_path.split(self.ATTR_AK_PATH_SPLIT_CHAR):
                data = data[k]

        return data

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
        sort_param_lists(self.i.p)
        sort_param_lists(self.e)

        # checking if changed
        for field in self.i.FIELDS_CHANGE:
            if field in self.i.p:
                if self.PARAM_MATCH_FIELDS in self.i.p:
                    if field in self.i.p[self.PARAM_MATCH_FIELDS]:
                        continue

                if hasattr(self.i, self.ATTR_FIELD_ID):
                    if field == getattr(self.i, self.ATTR_FIELD_ID):
                        continue

                try:
                    if str(self.e[field]) != str(self.i.p[field]):
                        self.i.r['changed'] = True

                        if self.i.p['debug']:
                            self.i.m.warn(
                                f"Field changed: '{field}' "
                                f"'{self.e[field]}' != '{self.i.p[field]}'"
                            )

                        break

                except KeyError:
                    exit_bug(
                        f"The field '{field}' seems to be unset - check the modules config!"
                    )

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
        cont_rel = self.i.API_CONT

        if hasattr(self.i, self.ATTR_REL_CONT):
            cont_rel = getattr(self.i, self.ATTR_REL_CONT)

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
            exit_bug('The diff-source object must be of type dict!')

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
        TRANSLATE_VALUES = {}
        BOOL_INVERT_FIELDS = []

        if ignore_fields is None:
            ignore_fields = []

        if is_unset(self.e):
            self.e = getattr(self.i, self.i.EXIST_ATTR)

        if hasattr(self.i, self.ATTR_TRANSLATE):
            TRANSLATE_FIELDS = getattr(self.i, self.ATTR_TRANSLATE)

        if hasattr(self.i, self.ATTR_BOOL_INVERT):
            BOOL_INVERT_FIELDS = getattr(self.i, self.ATTR_BOOL_INVERT)

        if hasattr(self.i, self.ATTR_VALUE_MAP):
            TRANSLATE_VALUES = getattr(self.i, self.ATTR_VALUE_MAP)

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

            if field in TRANSLATE_VALUES:
                try:
                    opn_data = TRANSLATE_VALUES[field][opn_data]

                except KeyError:
                    pass

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

        if hasattr(self.i, self.ATTR_AK_PATH_REQ):
            ak_path = getattr(self.i, self.ATTR_AK_PATH_REQ).split(self.ATTR_AK_PATH_SPLIT_CHAR)
            ak_path.reverse()

            for k in ak_path:
                payload = {k: payload}

        elif hasattr(self.i, self.ATTR_AK_PATH):
            # request only needs the last key
            ak_path = getattr(self.i, self.ATTR_AK_PATH)
            attr_ak = ak_path

            if ak_path.find('.') != -1:
                attr_ak = ak_path.rsplit(self.ATTR_AK_PATH_SPLIT_CHAR, 1)[1]

            payload = {attr_ak: payload}

        return payload

    def find_single_link(
            self, field: str, existing: dict, set_field: str = None, existing_field_id: str = 'name',
            fail: bool = True
    ) -> bool:
        entry = None

        if self.i.p[field] != '':
            found = False
            if set_field is None:
                set_field = field

            if len(existing) > 0:
                for uuid, item in existing.items():
                    if item[existing_field_id] == self.i.p[field]:
                        self.i.p[set_field] = uuid
                        entry = item[existing_field_id]
                        found = True

            if not found:
                if fail:
                    self.i.m.fail_json(
                        f"Provided {field} '{self.i.p[field]}' was not found!"
                    )

                return False

        if set_field in self.i.r['diff']['before']:
            self.i.r['diff']['before'][set_field] = entry

        return True

    def find_multiple_links(
            self, field: str, existing: dict, set_field: str = None, existing_field_id: str = 'name',
            fail: bool = True, fail_soft: bool = False
    ) -> bool:
        provided = len(self.i.p[field]) > 0
        uuids = []
        entries = []

        if not provided:
            return True

        if existing is not None and len(existing) > 0:
            for uuid, item in existing.items():
                if item[existing_field_id] in self.i.p[field]:
                    uuids.append(uuid)
                    entries.append(item[existing_field_id])

                if len(uuids) == len(self.i.p[field]):
                    break

        if len(uuids) != len(self.i.p[field]):
            msg = f"At least one of the provided {field} entries was not found!"

            if fail:
                self.i.m.fail_json(msg)

            if fail_soft:
                raise ModuleSoftError(msg)

            return False

        if set_field is None:
            set_field = field

        self.i.p[set_field] = uuids
        if set_field in self.i.r['diff']['before']:
            entries.sort()
            self.i.r['diff']['before'][set_field] = entries

            if set_field in self.i.r['diff']['after']:
                self.i.r['diff']['after'][set_field].sort()

        return True

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

        if hasattr(self.i, self.ATTR_VALUE_MAP_RCV):
            value_map = getattr(self.i, self.ATTR_VALUE_MAP_RCV)

        elif hasattr(self.i, self.ATTR_VALUE_MAP):
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
