from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class BaseModule:
    def __init__(self, m: AnsibleModule, r: dict, s: Session = None):
        self.m = m
        self.p = m.params
        self.r = r
        self.b = Base(instance=self)
        self.s = Session(module=m) if s is None else s
        self.exists = False
        self.existing_entries = None

    def _search_call(self) -> list:
        return self.b.search()

    def get_existing(self) -> list:
        return self.b.get_existing()

    def process(self):
        self.b.process()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
