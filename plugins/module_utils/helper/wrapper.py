
from inspect import stack as inspect_stack
from inspect import getfile as inspect_getfile

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler


def module_process(instance: BaseModule):
    instance.check()
    instance.process()
    if 'reload' in instance.m.params and instance.r['changed'] and instance.m.params['reload']:
        instance.reload()

    if hasattr(instance, 's'):
        instance.s.close()


def module_wrapper(instance: BaseModule):
    if instance.m.params['profiling'] or instance.m.params['debug']:
        module_name = inspect_getfile(inspect_stack()[1][0]).rsplit('/', 1)[1].rsplit('.', 1)[0]
        return profiler(check=module_process, module_name=module_name, kwargs={'instance': instance})

    return module_process(instance)
