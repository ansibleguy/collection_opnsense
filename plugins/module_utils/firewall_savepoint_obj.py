from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import single_post


class SavePoint:
    def __init__(self, module: AnsibleModule, result: dict, controller: str = None):
        self.m = module
        self.r = result
        self.c = controller if controller is not None else self.m.params['controller']
        self.revision = self.m.params['revision']
        self.call_cnf = {  # config shared by all calls
            'module': 'firewall',
            'controller': self.c,
        }

    def create(self) -> str:
        if self.revision is None:
            response = single_post(
                module=self.m,
                cnf={
                    'command': 'savepoint',
                    **self.call_cnf,
                }
            )

            if 'revision' not in response:
                self.m.fail_json(msg=f"Failed to create savepoint!")

            return response['revision']

        else:
            self.m.fail_json(f"Unable to create savepoint - a revision ('{self.revision}') exists!")

    def _check_revision(self, action: str):
        if self.revision is None:
            self.m.fail_json(f"Unable to run action '{action}' - a target revision needs to be provided!")

    def apply(self):
        self._check_revision(action='apply')
        single_post(
            module=self.m,
            cnf={
                'command': 'apply',
                'params': [self.revision],
                **self.call_cnf,
            }
        )

    def cancel_rollback(self):
        self._check_revision(action='cancel_rollback')
        single_post(
            module=self.m,
            cnf={
                'command': 'cancelRollback',
                'params': [self.revision],
                **self.call_cnf,
            }
        )

    def revert(self):
        self._check_revision(action='revert')
        single_post(
            module=self.m,
            cnf={
                'command': 'revert',
                'params': [self.revision],
                **self.call_cnf,
            }
        )
