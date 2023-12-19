from cProfile import Profile
from pstats import Stats
from io import StringIO
from datetime import datetime
from pathlib import Path
from typing import Callable
from inspect import stack as inspect_stack
from inspect import getfile as inspect_getfile

from httpx import ConnectError, ConnectTimeout

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
    DEBUG_CONFIG


def profiler(
        check: Callable, kwargs: dict, module_name: str = None,
        sort: str = 'tottime', show_top_n: int = 20
) -> (list, dict, bool, None):
    # note: https://stackoverflow.com/questions/10326936/sort-cprofile-output-by-percall-when-profiling-a-python-script
    # sort options: ncalls, tottime, cumtime
    _ = Profile()
    _.enable()

    if module_name is None:
        module_name = inspect_getfile(inspect_stack()[1][0]).rsplit('/', 1)[1].rsplit('.', 1)[0]

    httpx_error = None
    check_response = None

    try:
        check_response = check(**kwargs)

    except (ConnectError, ConnectTimeout, ConnectionError) as error:
        httpx_error = str(error)

    _.disable()
    result = StringIO()
    Stats(_, stream=result).sort_stats(sort).print_stats(show_top_n)
    cleaned_result = result.getvalue().splitlines()[:-1]
    del cleaned_result[1:5]
    cleaned_result = '\n'.join(cleaned_result)

    if module_name is not None:
        log_path = Path(DEBUG_CONFIG['path_log'])
        if not log_path.exists():
            log_path.mkdir()

        with open(f'{log_path}/{module_name}.log', 'a+', encoding='utf-8') as log:
            log.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')} | {cleaned_result}\n")

    else:
        print(cleaned_result)

    if httpx_error is not None:
        print(f"HTTP ERROR: {httpx_error}")

    return check_response
