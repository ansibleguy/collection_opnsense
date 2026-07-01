from inspect import stack as inspect_stack
from inspect import getfile as inspect_getfile

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.multi import \
    MultiModule, MultiModuleCallbacks
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.utils import profiler
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import diff_remove_empty


def _single_module_process(instance: BaseModule):
    instance.check()
    instance.process()
    if 'reload' in instance.m.params and instance.r['changed'] and instance.m.params['reload']:
        instance.reload()

    if hasattr(instance, 's'):
        instance.s.close()

    instance.r['diff'] = diff_remove_empty(instance.r['diff'])


def module_multi_wrapper(
        module: AnsibleModule, result: dict, obj: BaseModule, kind: str, entry_args: dict,
        callbacks: MultiModuleCallbacks = None,
):
    m = MultiModule(
        module=module,
        result=result,
        kind=kind,
        obj=obj,
        entry_args=entry_args['multi']['options'],
        callbacks=callbacks,
    )
    if module.params['profiling'] or module.params['debug']:
        module_name = inspect_getfile(inspect_stack()[1][0]).rsplit('/', 1)[1].rsplit('.', 1)[0]
        return profiler(check=m.process, module_name=module_name, kwargs={})

    # if the user wants to purge every entry - it makes no sense to hinder it for a single one
    if module.params['multi_control']['purge_all']:
        module.params['multi_control']['fail_process'] = False

    return m.process()


def module_wrapper(instance: BaseModule):
    if instance.m.params['profiling'] or instance.m.params['debug']:
        module_name = inspect_getfile(inspect_stack()[1][0]).rsplit('/', 1)[1].rsplit('.', 1)[0]
        return profiler(check=_single_module_process, module_name=module_name, kwargs={'instance': instance})

    return _single_module_process(instance)
