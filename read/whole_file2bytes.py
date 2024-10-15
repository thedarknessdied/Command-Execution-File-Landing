# -*- coding: utf-8 -*-


def read(
        path: str,
        *args, **kwargs
):
    with open(path, mode="rb") as f:
        _result = f.read()
    yield _result
