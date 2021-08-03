from is_iter import is_iter


def fork(condition, iterable, replacement=False):
    forked = []

    if isinstance(condition, dict):
        if replacement:
            forked = {k: fork(condition=c, iterable=iterable, replacement=replacement)[0] for k, c in condition.items()}
        else:
            # TODO insertion order isn't necessarily guaranteed
            # TODO check python version?
            raise NotImplementedError
        forked.update({None: [e for e in iterable if not any(e in f for f in forked.values())]})
    elif is_iter(condition):
        if replacement:
            forked.extend([fork(condition=c, iterable=iterable, replacement=replacement)[0] for c in condition])
        else:
            for c in condition:
                new_fork, iterable = fork(condition=c, iterable=iterable, replacement=replacement)
                forked.append(new_fork)
        forked.append([e for e in iterable if not any(e in f for f in forked)])
    elif callable(condition):
        forked.append(list(filter(condition, iterable)))
        forked.append([e for e in iterable if e not in forked[0]])
    elif condition is None:
        forked = fork(condition=lambda x: bool(x), iterable=iterable)
    else:
        raise NotImplementedError

    return forked
