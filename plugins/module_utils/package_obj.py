from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session


class Package:
    def __init__(self, module: AnsibleModule, name: str, session: Session = None):
        self.m = module
        self.s = Session(module=module) if session is None else session
        self.n = name
        self.r = {
            'changed': False, 'version': None,
            'diff': {'before': {'installed': False, 'locked': False}}
        }
        self.call_cnf = {  # config shared by all calls
            'module': 'firewall',
            'controller': 'alias',
        }
        self.package_stati = None
        self.call_cnf = {
            'module': 'core',
            'controller': 'firmware',
        }

    def check(self):
        if self.package_stati is None:
            self.package_stati = self.search_call()

        for pkg_status in self.package_stati:
            if pkg_status['name'] == self.n:
                if self.m.params['debug']:
                    self.m.warn(f"Package status: '{pkg_status}'")

                self.r['diff']['before']['version'] = pkg_status['version']

                if pkg_status['installed'] in ['1', 1, True]:
                    self.r['diff']['before']['installed'] = True

                if pkg_status['locked'] in ['1', 1, True]:
                    self.r['diff']['before']['locked'] = True

        self.r['diff']['after'] = self.r['diff']['before'].copy()
        self.lock_check()
        self.call_cnf['params'] = [self.n]

    def lock_check(self):
        if self.m.params['action'] in ['reinstall', 'remove', 'install'] and \
                self.r['diff']['before']['locked']:
            self.m.fail_json(
                f"Unable to execute action '{self.m.params['action']}' - "
                f"package is locked!"
            )

    def search_call(self) -> dict:
        return self.s.get(cnf={'command': 'info', **self.call_cnf})['package']

    def change_state(self):
        run = False

        if self.m.params['action'] == 'lock':
            if not self.r['diff']['before']['locked']:
                run = True
                self.r['diff']['after']['locked'] = True

        elif self.m.params['action'] == 'unlock':
            if self.r['diff']['before']['locked']:
                run = True
                self.r['diff']['after']['locked'] = False

        elif self.m.params['action'] == 'remove':
            self.r['diff']['after']['installed'] = False
            run = True

        else:
            run = True

        self.r['changed'] = True
        if not self.m.check_mode and run:
            self.execute()

    def execute(self):
        if not self.m.check_mode:
            self.s.post(cnf={
                'command': self.m.params['action'],
                **self.call_cnf
            })

    def install(self):
        self.r['changed'] = True
        self.r['diff']['after']['installed'] = True
        self.execute()
