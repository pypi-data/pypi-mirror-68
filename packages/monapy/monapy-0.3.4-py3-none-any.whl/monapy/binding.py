# -*- coding: utf-8 -*-

from itertools import chain
from functools import partial
from functools import reduce


class Binder:
    def __init__(self):
        self._func_chain = []

    def __rshift__(self, obj):
        return self.bind(obj)

    def __lshift__(self, obj):
        return self.lbind(obj)

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def bind(self, obj):
        if hasattr(obj, '__call__'):
            self._func_chain.append(obj)
        else:
            raise TypeError('Must be callable')
        return self

    def lbind(self, obj):
        _func = self._func_chain.pop()
        self._func_chain.append(partial(_func, obj))
        return self

    def call(self, *args, **kwargs):
        if not self._func_chain:
            if args:
                return args[0]
            else:
                return
        first_func = self._func_chain[0]
        other_funcs = self._func_chain[1:]
        return reduce(
            lambda val, func: func(val),
            chain(
                [first_func(*args, **kwargs)],
                other_funcs
            )
        )
