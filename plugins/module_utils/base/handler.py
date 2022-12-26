MODULE_EXCEPTIONS = (ModuleNotFoundError, ImportError)


def module_dependency_error():
    raise ModuleNotFoundError(
        'For this Ansible-module to work you must install its dependencies first: '
        "'python3 -m pip install httpx'"
    )


class ModuleSoftError(Exception):
    pass
