from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.arg_spec import ModuleArgumentSpecValidator


def validate_single(
        module: AnsibleModule, module_args: dict, log_mod: str,
        key: (int, str), cnf: dict) -> bool:
    result = False

    validation = ModuleArgumentSpecValidator(module_args,
                                             module.mutually_exclusive,
                                             module.required_together,
                                             module.required_one_of,
                                             module.required_if,
                                             module.required_by
                                             ).validate(parameters=cnf)

    try:
        validation_error = validation.errors[0]

    except IndexError:
        validation_error = None

    if validation_error:
        error_msg = validation.errors.msg
        if module.params['fail_verification']:
            module.fail_json(f"Got invalid config for {log_mod} '{key}': {error_msg}")

        else:
            module.warn(f"Got invalid config for {log_mod} '{key}': {error_msg}")

    else:
        result = True

    return result


def convert_aliases(cnf: dict, aliases: dict) -> dict:
    # would be done by ansible-module in default-modules
    converted = {}

    for _param, _aliases in aliases.items():
        value = cnf[_param] if _param in cnf else None

        if value is None:
            for alias in _aliases:
                if alias in cnf:
                    value = cnf[alias]
                    break

        if value is not None:
            converted[_param] = value

    return converted
