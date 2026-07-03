# pylint: disable=R0912,R0915
from abc import abstractmethod

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import single_get, single_post, Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import to_digit, is_unset, sort_param_lists
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import get_simple_existing, \
    simplify_translate
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.match import get_matching
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import exit_bug, ModuleSoftError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    validate_int_fields, validate_str_fields


class BaseLogic:
    DIFF_FLOAT_ROUND = 1
    RESP_JOIN_CHAR = ','
    ATTR_JOIN_CHAR = 'JOIN_CHAR'
    ATTR_AK_PATH = 'API_KEY_PATH'
    ATTR_AK_PATH_REQ = 'API_KEY_PATH_REQ'
    ATTR_AK_PATH_GET = 'API_KEY_PATH_GET'
    ATTR_GET_ADD = 'SEARCH_ADDITIONAL'
    ATTR_GET_DETAIL_ALL = 'SEARCH_DETAIL_ALL'
    ATTR_AK_PATH_SPLIT_CHAR = '.'
    ATTR_BOOL_INVERT = 'FIELDS_BOOL_INVERT'
    ATTR_OPTIONAL = 'FIELDS_OPTIONAL'
    ATTR_TRANSLATE = 'FIELDS_TRANSLATE'
    ATTR_DIFF_EXCL = 'FIELDS_DIFF_EXCLUDE'
    ATTR_DIFF_NO_LOG = 'FIELDS_DIFF_NO_LOG'
    ATTR_VALUE_MAP = 'FIELDS_VALUE_MAPPING'
    ATTR_VALUE_MAP_RCV = 'FIELDS_VALUE_MAPPING_RCV'
    ATTR_FIELD_ALL = 'FIELDS_ALL'
    ATTR_FIELD_CH = 'FIELDS_CHANGE'
    ATTR_REL_CONT = 'API_CONT_REL'
    ATTR_REL_CMD = 'API_CMD_REL'
    ATTR_GET_CONT = 'API_CONT_GET'
    ATTR_GET_MOD = 'API_MOD_GET'
    ATTR_API_MOD = 'API_MOD'
    ATTR_API_CONT = 'API_CONT'
    ATTR_HEADERS = 'call_headers'
    ATTR_TYPING = 'FIELDS_TYPING'
    ATTR_FIELD_ID = 'FIELD_ID'
    ATTR_FIELD_PK = 'FIELD_PK'
    ATTR_CMDS = 'CMDS'
    ATTR_EXIST = 'EXIST_ATTR'
    PARAM_MATCH_FIELDS = 'match_fields'
    QUERY_MAX_ENTRIES = 1000
    VALUE_NO_LOG = 'VALUE_SPECIFIED_IN_NO_LOG_PARAMETER'

    REQUIRED_ATTRS = [
        ATTR_AK_PATH,
        ATTR_TYPING,
        ATTR_API_MOD,
        ATTR_API_CONT,
        ATTR_FIELD_ALL,
        ATTR_FIELD_CH,
        ATTR_CMDS,
    ]

    def __init__(self, m, r: dict, s: Session = None):
        if hasattr(self, 'TIMEOUT'):
            self.s = Session(module=m, timeout=self.TIMEOUT) if s is None else s
        else:
            self.s = Session(module=m) if s is None else s

        self.m = m
        self.p = m.params
        self.r = r
        self.e = {}
        self.raw = None
        self.exists = False
        self.existing_entries = None

        if not hasattr(self, self.ATTR_EXIST):
            self.EXIST_ATTR = 'existing_entries'

        for attr in self.REQUIRED_ATTRS:
            if not hasattr(self, attr) or getattr(self, attr) is None:
                exit_bug(f"Module has no '{attr}' attribute set!")

        self._init_defaults()

    def _init_defaults(self):
        if not hasattr(self, self.ATTR_API_MOD):
            self.API_MOD = None

        if not hasattr(self, self.ATTR_API_CONT):
            self.API_CONT = None

        if not hasattr(self, self.ATTR_CMDS):
            self.CMDS = {}

        if not hasattr(self, self.ATTR_FIELD_ALL):
            self.FIELDS_ALL = []

        if not hasattr(self, self.ATTR_FIELD_CH):
            self.FIELDS_CHANGE = []

        self.call_cnf = {
            'module': getattr(self, self.ATTR_API_MOD, None),
            'controller': getattr(self, self.ATTR_API_CONT, None),
        }

    # --- Core Logic ---
    def _check_validators(self):
        if 'state' in self.p and self.p['state'] != 'present':
            return

        if hasattr(self, 'STR_VALIDATIONS'):
            if hasattr(self, 'STR_LEN_VALIDATIONS'):
                validate_str_fields(
                    module=self.m,
                    data=self.p,
                    field_regex=self.STR_VALIDATIONS,
                    field_minmax_length=self.STR_LEN_VALIDATIONS
                )

            else:
                validate_str_fields(module=self.m, data=self.p, field_regex=self.STR_VALIDATIONS)

        elif hasattr(self, 'STR_LEN_VALIDATIONS'):
            validate_str_fields(module=self.m, data=self.p, field_minmax_length=self.STR_LEN_VALIDATIONS)

        if hasattr(self, 'INT_VALIDATIONS'):
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

    @abstractmethod
    def check(self) -> None:
        pass

    def get_existing(self) -> list[dict]:
        return self._base_get_existing()

    def process(self) -> None:
        self._base_process()

    def create(self) -> dict:
        return self._base_create()

    def update(self) -> dict:
        return self._base_update()

    def delete(self) -> dict:
        return self._base_delete()

    def reload(self) -> dict:
        return self._base_reload()

    def api_search_post(self, cnf: dict, data: dict = None) -> list:
        if data is None:
            data = {}

        return self._api_post({
            **cnf,
            'data': {'current': 1, 'rowCount': self.QUERY_MAX_ENTRIES, **data},
        })['rows']

    def search(self, match_fields: list = None) -> (dict, list):
        # workaround if 'get' needs to be performed using other api module/controller
        cont_get, mod_get = self.API_CONT, self.API_MOD

        if hasattr(self, self.ATTR_GET_CONT):
            cont_get = getattr(self, self.ATTR_GET_CONT)

        if hasattr(self, self.ATTR_GET_MOD):
            mod_get = getattr(self, self.ATTR_GET_MOD)

        self.call_cnf['controller'] = cont_get
        self.call_cnf['module'] = mod_get

        if self.CMDS['search'].startswith('search'):
            # because of new OPNsense API: https://github.com/O-X-L/ansible-opnsense/issues/51
            if 'detail' not in self.CMDS:
                exit_bug("To use the 'search' commands you need to also define the related 'detail' (get) command!")

            data = []
            # if we can - we only perform the 'detail' call for the already matched entry to save on needed requests
            base_match_fields = False
            base_match_fields_checked = False
            force_details = getattr(self, self.ATTR_GET_DETAIL_ALL, False)

            for base_entry in self.api_search_post({
                **self.call_cnf,
                'command': self.CMDS['search'],
            }):
                if not force_details and match_fields is not None and not base_match_fields_checked:
                    base_match_fields_checked = True
                    base_match_fields = all(field in base_entry for field in match_fields)

                # todo: perform async calls for parallel data fetching
                detail_entry = {}
                if force_details or not base_match_fields or \
                        all(base_entry[field] == self.p[field] for field in match_fields):
                    detail_entry = self._search_path_handling(
                        self._api_get({
                            **self.call_cnf,
                            'command': self.CMDS['detail'],
                            'params': [base_entry[self.field_pk]]
                        })
                    )
                    if self.raw is None:
                        self.raw = detail_entry

                data.append({
                    **base_entry,
                    **detail_entry,
                })

            if self.raw is None:
                self.raw = self._search_path_handling(
                    self._api_get({
                        **self.call_cnf,
                        'command': self.CMDS['detail'],
                    })
                )

            return data

        # legacy api handling (fewer requests needed; much simpler client-side handling)
        data = self._api_get({
            **self.call_cnf,
            'command': self.CMDS['search'],
        })

        if hasattr(self, self.ATTR_GET_ADD):
            for attr, ak_path in getattr(self, self.ATTR_GET_ADD).items():
                if hasattr(self, attr):
                    setattr(
                        self, attr,
                        self._search_path_handling(data=data, ak_path=ak_path)
                    )

        return self._search_path_handling(data)

    def _search_path_handling(self, data: dict, ak_path: str = None) -> dict:
        # resolving API_KEY_PATH's so data from nested dicts gets extracted as configured
        if ak_path is None:
            if hasattr(self, self.ATTR_AK_PATH_GET):
                ak_path = getattr(self, self.ATTR_AK_PATH_GET)

            elif hasattr(self, self.ATTR_AK_PATH):
                ak_path = getattr(self, self.ATTR_AK_PATH)

        try:
            if ak_path is not None:
                for k in ak_path.split(self.ATTR_AK_PATH_SPLIT_CHAR):
                    data = data[k]

            return data

        except KeyError:
            exit_bug(f"Got invalid API_KEY_PATH: '{ak_path}' not matching data '{data}'")
            return {}

    def _base_get_existing(self, diff_filter: bool = False, details_all: bool = True) -> list[dict]:
        if details_all:
            # because of new OPNsense API: https://github.com/O-X-L/ansible-opnsense/issues/51
            # we require all details even if that means we have to perform hundreds of api-calls.. :(
            setattr(self, self.ATTR_GET_DETAIL_ALL, True)

        if diff_filter:
            # use already existing filtering to get 'clean' int/.. values
            return get_simple_existing(
                entries=self._call_search(),
                simplify_func=self.simplify_existing,
                add_filter=self.build_diff,
            )

        return get_simple_existing(
            entries=self._call_search(),
            simplify_func=self.simplify_existing,
        )

    def find(self, match_fields: list) -> None:
        if self.existing_entries is None:
            self.existing_entries = self._call_search(match_fields)

        match = get_matching(
            module=self.m,
            existing_items=self.existing_entries,
            compare_item=self.p,
            match_fields=match_fields,
            simplify_func=self.simplify_existing,
        )

        if match is not None:
            setattr(self, self.EXIST_ATTR, match)
            self.exists = True
            self.r['diff']['before'] = self.build_diff(data=match)

            if self.field_pk in match:
                self.call_cnf['params'] = [match[self.field_pk]]

    def _base_process(self) -> None:
        self.call_cnf['controller'] = self.API_CONT
        self.call_cnf['module'] = self.API_MOD

        if 'state' in self.p and self.p['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if 'state' not in self.p or self.exists:
                self.update()

            else:
                self.create()

    def _base_create(self) -> dict:
        self.r['changed'] = True

        if not self.m.check_mode:
            return self._api_post({
                **self.call_cnf,
                'command': self.CMDS['add'],
                'data': self._get_request_data(),
            })

        return {}

    def _base_update(self, enable_switch: bool = True) -> dict:
        self._set_existing()
        sort_param_lists(self.p)
        sort_param_lists(self.e)

        # checking if changed
        for field in self.FIELDS_CHANGE:
            if field in self.p:
                if self.PARAM_MATCH_FIELDS in self.p:
                    if field in self.p[self.PARAM_MATCH_FIELDS]:
                        continue

                if field == getattr(self, self.ATTR_FIELD_ID, None):
                    continue

                if field in getattr(self, self.ATTR_OPTIONAL, []) and field not in self.e:
                    # OPNsense API may conditionally omit some fields from API-responses :(
                    continue

                try:
                    if self.p[field] is None:
                        self.p[field] = ''

                    if str(self.e[field]) != str(self.p[field]):
                        self.r['changed'] = True

                        if self.p['debug']:
                            self.m.warn(
                                f"Field changed: '{field}' "
                                f"'{self.e[field]}' != '{self.p[field]}'"
                            )

                        break

                except KeyError:
                    exit_bug(
                        f"The field '{field}' seems to be unset - check the modules config!"
                    )

        # update if changed
        if self.r['changed']:
            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

            if not self.m.check_mode:
                if hasattr(self, '_update_call'):
                    response = self._update_call()

                else:
                    response = self._api_post({
                        **self.call_cnf,
                        'command': self.CMDS['set'],
                        'data': self._get_request_data(),
                    })

                if self.p['debug']:
                    self.m.warn(f"{self.r['diff']}")

                return response

        elif enable_switch:
            self._base_update_enabled()

        return {}

    def _base_update_enabled(self) -> None:
        existing = getattr(self, self.EXIST_ATTR)

        if 'enabled' not in existing or 'enabled' not in self.p or existing['enabled'] == self.p['enabled']:
            return

        should_be_enabled = self.p['enabled']
        invert = False

        if 'enabled' in getattr(self, self.ATTR_BOOL_INVERT, []):
            invert = True
            should_be_enabled = not should_be_enabled

        if should_be_enabled:
            self.enable(invert=invert)

        else:
            self.disable(invert=invert)

    def _base_delete(self) -> dict:
        self.r['changed'] = True
        self.r['diff']['after'] = {}

        if not self.m.check_mode:
            if hasattr(self, '_delete_call'):
                response = self._delete_call()

            else:
                response = self._api_post({
                    **self.call_cnf,
                    'command': self.CMDS['del'],
                })

            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

            return response

        return {}

    def _base_reload(self) -> dict:
        # reload the running config
        cont_rel = self.API_CONT
        cmd_rel = 'reconfigure'

        if hasattr(self, self.ATTR_REL_CONT):
            cont_rel = getattr(self, self.ATTR_REL_CONT)

        if hasattr(self, self.ATTR_REL_CMD):
            cmd_rel = getattr(self, self.ATTR_REL_CMD)

        if not self.m.check_mode:
            return self._api_post({
                'module': self.API_MOD,
                'controller': cont_rel,
                'command': cmd_rel,
                'params': []
            })

        return {}

    def _get_request_data(self) -> dict:
        if hasattr(self, 'build_request'):
            return self.build_request()

        return self._base_build_request()

    def _change_enabled_state(self) -> dict:
        return self._api_post({
            **self.call_cnf,
            'command': self.CMDS['toggle'],
            'params': [getattr(self, self.EXIST_ATTR)[self.field_pk]],
        })

    def is_enabled(self, invert: bool = False) -> bool:
        # if the translated entry from the OPNsense-API is enabled
        is_enabled = getattr(self, self.EXIST_ATTR)['enabled']

        if invert:
            is_enabled = not is_enabled

        return is_enabled

    def enable(self, invert: bool = False) -> dict:
        if self.exists and not self.is_enabled(invert=invert):
            self.r['changed'] = True
            if not invert:
                self.r['diff']['before'] = {'enabled': False}
                self.r['diff']['after'] = {'enabled': True}

            else:
                self.r['diff']['before'] = {'enabled': True}
                self.r['diff']['after'] = {'enabled': False}

            if not self.m.check_mode:
                return self._change_enabled_state()

        return {}

    def disable(self, invert: bool = False) -> dict:
        if self.exists and self.is_enabled(invert=invert):
            self.r['changed'] = True
            if not invert:
                self.r['diff']['before'] = {'enabled': True}
                self.r['diff']['after'] = {'enabled': False}

            else:
                self.r['diff']['before'] = {'enabled': False}
                self.r['diff']['after'] = {'enabled': True}

            if not self.m.check_mode:
                return self._change_enabled_state()

        return {}

    def build_diff(self, data: dict) -> dict:
        if not isinstance(data, dict):
            exit_bug('The diff-source object must be of type dict!')

        _exclude_fields = []
        _no_log_fields = []

        if hasattr(self, self.ATTR_DIFF_EXCL):
            _exclude_fields = getattr(self, self.ATTR_DIFF_EXCL)

        if hasattr(self, self.ATTR_DIFF_NO_LOG):
            _no_log_fields = getattr(self, self.ATTR_DIFF_NO_LOG)

        self._set_existing()

        diff = {
            self.field_pk: self.e[self.field_pk] if self.field_pk in self.e else None
        }

        for field in self.FIELDS_ALL:
            if field in _exclude_fields:
                continue

            if field in _no_log_fields:
                diff[field] = self.VALUE_NO_LOG
                continue

            stringify = True

            try:
                diff[field] = data[field]

            except KeyError:
                if field in self.p:
                    diff[field] = self.p[field]

            if isinstance(diff[field], list):
                try:
                    diff[field].sort()

                except TypeError:
                    raise exit_bug(f"Field not defined as 'select_opt_list' type: {diff[field]}")

                stringify = False

            elif isinstance(diff[field], str) and diff[field].isnumeric:
                try:
                    diff[field] = int(diff[field])
                    stringify = False

                except (TypeError, ValueError):
                    pass

            elif isinstance(diff[field], dict) and self.field_pk in diff[field]:
                diff[field] = diff[field][self.field_pk]

            elif isinstance(diff[field], (bool, int)):
                stringify = False

            elif diff[field] is None:
                diff[field] = ''

            if stringify:
                try:
                    diff[field] = round(float(diff[field]), self.DIFF_FLOAT_ROUND)
                    stringify = False

                except (TypeError, ValueError):
                    pass

            if stringify:
                diff[field] = str(diff[field])

        return diff

    def _base_build_request(self, ignore_fields: list = None) -> dict:
        ignore_fields = ignore_fields or []
        request = {}

        if is_unset(self.e):
            self.e = getattr(self, self.EXIST_ATTR)

        _translate_fields = getattr(self, self.ATTR_TRANSLATE, {})

        for field in self.FIELDS_ALL:
            if field in ignore_fields:
                continue

            opn_field = _translate_fields.get(field, field)
            raw_data = self._build_request_extract_raw_data(field)
            formatted_data = self._build_request_format_data(field, raw_data)
            self._build_request_handle_field_name_translation(request, opn_field, formatted_data)

        return self._build_request_wrap_payload(request)

    def _build_request_extract_raw_data(self, field: str):
        """Retrieves the raw data for a given field from priority sources."""
        if field in getattr(self, 'p', {}):
            return self.p[field]

        if field in self.e:
            return self.e[field]

        return ''

    def _build_request_format_data(self, field: str, opn_data):
        """Handles value translation, boolean inversion, list joining, and null checks."""
        _translate_values = getattr(self, self.ATTR_VALUE_MAP, {})
        _bool_invert_fields = getattr(self, self.ATTR_BOOL_INVERT, [])

        # Value Translation
        if field in _translate_values and opn_data in _translate_values[field]:
            opn_data = _translate_values[field][opn_data]

        # Type-specific formatting
        if isinstance(opn_data, bool):
            if field in _bool_invert_fields:
                opn_data = not opn_data

            return to_digit(opn_data)

        if isinstance(opn_data, list):
            join_char = getattr(self, self.ATTR_JOIN_CHAR, self.RESP_JOIN_CHAR)
            return join_char.join(opn_data)

        if opn_data is None:
            return ''

        return opn_data

    @staticmethod
    def _build_request_handle_field_name_translation(request: dict, opn_field, value):
        """Safely assigns a value to a flat key, nested tuple path, or list fallback."""
        if isinstance(opn_field, tuple) and len(opn_field) > 0:
            current_level = request
            for key in opn_field[:-1]:
                current_level = current_level.setdefault(key, {})

            current_level[opn_field[-1]] = value

        elif isinstance(opn_field, list) and len(opn_field) > 0:
            request[opn_field[0]] = value

        else:
            request[opn_field] = value

    def _build_request_wrap_payload(self, payload: dict) -> dict:
        """Wraps the fully built request dictionary in the required outer AK paths."""
        if hasattr(self, self.ATTR_AK_PATH_REQ):
            ak_path = getattr(self, self.ATTR_AK_PATH_REQ).split(self.ATTR_AK_PATH_SPLIT_CHAR)
            for k in reversed(ak_path):
                payload = {k: payload}

        elif hasattr(self, self.ATTR_AK_PATH):
            ak_path = getattr(self, self.ATTR_AK_PATH)
            attr_ak = ak_path.rsplit(self.ATTR_AK_PATH_SPLIT_CHAR, 1)[1] if '.' in ak_path else ak_path
            payload = {attr_ak: payload}

        return payload

    def find_single_link(self, field: str, existing: dict, set_field: str = None, existing_field_id: str = 'name',
                         fail: bool = True) -> bool:
        entry = None

        if not is_unset(self.p[field]):
            found = False
            if set_field is None:
                set_field = field

            if len(existing) > 0:
                for uuid, item in existing.items():
                    if item[existing_field_id] == self.p[field]:
                        self.p[set_field] = uuid
                        entry = item[existing_field_id]
                        found = True

            if not found:
                if fail:
                    if self.p['debug']:
                        self.m.warn(f"Unable to find link by field '{field}': '{self.p[field]}' in '{existing}'")

                    self.m.fail_json(
                        f"Provided {field} '{self.p[field]}' was not found!"
                    )

                return False

        if 'before' in self.r['diff'] and set_field in self.r['diff']['before']:
            self.r['diff']['before'][set_field] = entry

        return True

    def find_multiple_links(self, field: str, existing: dict, set_field: str = None, existing_field_id: str = 'name',
                            fail: bool = True, fail_soft: bool = False) -> bool:
        provided = len(self.p[field]) > 0
        uuids = []
        entries = []

        if not provided:
            return True

        if existing is not None and len(existing) > 0:
            for uuid, item in existing.items():
                if item[existing_field_id] in self.p[field]:
                    uuids.append(uuid)
                    entries.append(item[existing_field_id])

                if len(uuids) == len(self.p[field]):
                    break

        if len(uuids) != len(self.p[field]):
            msg = f"At least one of the provided {field} entries was not found!"

            if fail:
                self.m.fail_json(msg)

            if fail_soft:
                raise ModuleSoftError(msg)

            return False

        if set_field is None:
            set_field = field

        self.p[set_field] = uuids
        if set_field in self.r['diff']['before']:
            entries.sort()
            self.r['diff']['before'][set_field] = entries

            if set_field in self.r['diff']['after']:
                self.r['diff']['after'][set_field].sort()

        return True

    def _set_existing(self) -> None:
        if is_unset(self.e):
            _existing = getattr(self, self.EXIST_ATTR)

            if _existing is not None and len(_existing) > 0:
                self.e = _existing

    def simplify_existing(self, existing: dict) -> dict:
        return self._base_simplify_existing(existing)

    def _base_simplify_existing(self, existing: dict) -> dict:
        translate = getattr(self, self.ATTR_TRANSLATE, {})
        typing = getattr(self, self.ATTR_TYPING, {})
        bool_invert = getattr(self, self.ATTR_BOOL_INVERT, [])
        optional = getattr(self, self.ATTR_OPTIONAL, [])
        value_map = getattr(self, self.ATTR_VALUE_MAP_RCV, getattr(self, self.ATTR_VALUE_MAP, {}))

        return simplify_translate(
            existing=existing,
            typing=typing,
            translate=translate,
            value_map=value_map,
            bool_invert=bool_invert,
            optional=optional,
        )

    @property
    def field_pk(self) -> str:
        return getattr(self, self.ATTR_FIELD_PK, 'uuid')

    def _call_search(self, match_fields: list = None) -> (list, dict):
        if hasattr(self, 'search_call'):
            return self.search_call()

        return self.search(match_fields)

    def _api_headers(self) -> dict:
        return getattr(self, self.ATTR_HEADERS, {})

    def _api_post(self, cnf: dict) -> (dict, list):
        if hasattr(self, 's'):
            return self.s.post(
                cnf=cnf,
                headers=self._api_headers()
            )

        return single_post(
            cnf=cnf,
            module=self.m,
            headers=self._api_headers()
        )

    def _api_get(self, cnf: dict) -> (dict, list):
        if hasattr(self, 's'):
            return self.s.get(cnf=cnf)

        return single_get(
            cnf=cnf,
            module=self.m
        )
