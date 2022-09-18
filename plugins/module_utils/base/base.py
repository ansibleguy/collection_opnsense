# could be implemented using inheritance in the future..

# pylint: disable=W0212,R0912

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    single_get, single_post
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_simple_existing, to_digit, get_matching


class Base:
    DIFF_FLOAT_ROUND = 1
    RESP_JOIN_CHAR = ','

    def __init__(self, instance):
        self.i = instance  # module-specific object
        self.e = {}  # existing entry

    def search(self) -> (dict, list):
        if hasattr(self.i, 'API_KEY_2'):
            return self.i.s.get(cnf={
                **self.i.call_cnf, **{'command': self.i.CMDS['search']}
            })[self.i.API_KEY_1][self.i.API_KEY_2][self.i.API_KEY]

        return self.i.s.get(cnf={
            **self.i.call_cnf, **{'command': self.i.CMDS['search']}
        })[self.i.API_KEY_1][self.i.API_KEY]

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._call_search(),
            simplify_func=self._call_simple(),
        )

    def detail(self) -> (dict, list):
        return self.i.s.get(cnf={
            **self.i.call_cnf, **{'command': self.i.CMDS['detail']}
        })[self.i.API_KEY]

    def find(self, match_fields: list):
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
        if self.i.p['state'] == 'absent':
            if self.i.exists:
                self.i.delete()

        else:
            if self.i.exists:
                self.i.update()

            else:
                self.i.create()

    def create(self) -> dict:
        self.i.r['changed'] = True

        if not self.i.m.check_mode:
            return self.i.s.post(cnf={
                **self.i.call_cnf, **{
                    'command': self.i.CMDS['add'],
                    'data': self._get_request_data(),
                }
            })

    def update(self, enable_switch: bool = False) -> dict:
        if len(self.e) == 0:
            self.e = getattr(self.i, self.i.EXIST_ATTR)

        # checking if changed
        for field in self.i.FIELDS_CHANGE:
            if field in self.i.p:
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
            if getattr(self.i, self.i.EXIST_ATTR)['enabled'] != self.i.p['enabled']:
                if self.i.p['enabled']:
                    if hasattr(self.i, 'enable'):
                        self.i.enable()

                    else:
                        self.enable()

                else:
                    if hasattr(self.i, 'disable'):
                        self.i.disable()

                    else:
                        self.disable()

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
        if hasattr(self.i, 'API_CONT_REL'):
            cont_rel = self.i.API_CONT_REL

        else:
            cont_rel = self.i.API_CONT

        if not self.i.m.check_mode:
            return self.i.s.post(cnf={
                'module': self.i.API_MOD,
                'controller': cont_rel,
                'command': self.i.API_CMD_REL,
                'params': []
            })

    def _get_request_data(self):
        if hasattr(self.i, '_build_request'):
            return self.i._build_request()

        else:
            return self.build_request()

    def _change_enabled_state(self, value: int) -> dict:
        return self._api_post(cnf={
            **self.i.call_cnf, **{
                'command': self.i.CMDS['toggle'],
                'params': [getattr(self.i, self.i.EXIST_ATTR)['uuid'], value],
            }
        })

    def enable(self) -> dict:
        if self.i.exists and not getattr(self.i, self.i.EXIST_ATTR)['enabled']:
            self.i.r['changed'] = True
            self.i.r['diff']['before'] = {'enabled': False}
            self.i.r['diff']['after'] = {'enabled': True}

            if not self.i.m.check_mode:
                return self._change_enabled_state(1)

    def disable(self) -> dict:
        if self.i.exists and getattr(self.i, self.i.EXIST_ATTR)['enabled']:
            self.i.r['changed'] = True
            self.i.r['diff']['before'] = {'enabled': True}
            self.i.r['diff']['after'] = {'enabled': False}

            if not self.i.m.check_mode:
                return self._change_enabled_state(0)

    def build_diff(self, data: dict) -> dict:
        if len(self.e) == 0:
            self.e = getattr(self.i, self.i.EXIST_ATTR)

        if not isinstance(self.e, dict):
            raise ValueError('The existing attribute must be of type dict!')

        diff = {
            'uuid': self.e['uuid'] if 'uuid' in self.e else None
        }

        for field in self.i.FIELDS_ALL:
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

    def build_request(self) -> dict:
        request = {}
        translate = {}

        if len(self.e) == 0:
            self.e = getattr(self.i, self.i.EXIST_ATTR)

        if hasattr(self.i, 'FIELDS_TRANSLATE'):
            translate = self.i.FIELDS_TRANSLATE

        for field in self.i.FIELDS_ALL:
            opn_field = field
            if field in translate:
                opn_field = translate[field]

            if field in self.i.p:
                opn_data = self.i.p[field]

            else:
                opn_data = self.e[field]

            if isinstance(opn_data, bool):
                request[opn_field] = to_digit(opn_data)

            elif isinstance(opn_data, list):
                join_char = self.RESP_JOIN_CHAR

                if hasattr(self.i, 'JOIN_CHAR'):
                    join_char = self.i.JOIN_CHAR

                request[opn_field] = join_char.join(opn_data)

            else:
                request[opn_field] = opn_data

        return {self.i.API_KEY: request}

    def _call_search(self) -> (dict, list):
        call_search = self.search

        if hasattr(self.i, '_search_call'):
            call_search = self.i._search_call

        elif hasattr(self.i, 'search_call'):
            call_search = self.i.search_call

        return call_search()

    def _call_simple(self):
        if hasattr(self.i, 'simplify_existing'):
            call_simple = self.i.simplify_existing

        else:
            call_simple = self.i._simplify_existing

        return call_simple

    def _api_post(self, cnf: dict) -> (dict, list):
        if hasattr(self.i, 's'):
            return self.i.s.post(cnf=cnf)

        else:
            return single_post(cnf=cnf, module=self.i.m)

    def _api_get(self, cnf: dict) -> (dict, list):
        if hasattr(self.i, 's'):
            return self.i.s.get(cnf=cnf)

        else:
            return single_get(cnf=cnf, module=self.i.m)
