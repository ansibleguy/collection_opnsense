

def diff_remove_empty(diff: dict) -> dict:
    d = diff.copy()
    for k in diff.keys():
        if len(diff[k]) == 0:
            d.pop(k)

    return d


def ensure_list(data: (int, str, list)) -> list:
    # if user supplied a string instead of a list => convert it to match our expectations
    if isinstance(data, list):
        return data

    return [data]
