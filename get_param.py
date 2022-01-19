import re
from typing import Iterator


def get_param(f: Iterator, query_param: str) -> Iterator:
    res: Iterator
    ind: int
    query = query_param.split('|')
    res = map(lambda v: v.strip(), f)

    for item in query:
        query_split = item.split(':')
        cmd = query_split[0]
        if cmd == "filter":
            val = query_split[1]
            res = filter(lambda v: val in v, res)
        if cmd == "map":
            val = query_split[1]
            res = map(lambda v: v.split(' ')[int(val)], res)
        if cmd == "unique":
            res = iter(set(res))
        if cmd == "sort":
            val = query_split[1]
            if val == 'desc':
                res = iter(sorted(res, reverse=True))
            else:
                res = iter(sorted(res))
        if cmd == "limit":
            val = query_split[1]
            res = limit_func(res, int(val))
        if cmd == "regex":
            val = query_split[1]
            r = re.compile(val)
            res = filter(lambda v: r.search(v), res)
    return res


def limit_func(f: Iterator, limit: int) -> Iterator:
    i = 0
    for item in f:
        if i < limit:
            yield item
        else:
            break
        i += 1
