import persistent
import sys


def simpleWrapper(name):
    def wrapper(self, *args, **kwargs):
        return getattr(self._data, name)(*args, **kwargs)
    return wrapper


def mutatingWrapper(name):
    def wrapper(self, *args, **kwargs):
        res = getattr(self._data, name)(*args, **kwargs)
        self._p_changed = True
        return res
    return wrapper


def mutatingStrippingWrapper(name):
    def wrapper(self, other):
        if isinstance(other, self.__class__):
            other = other._data
        getattr(self._data, name)(other)
        self._p_changed = True
        return self  # this is used necessary for all the __i*__, so we have to
        # return the mutated value
    return wrapper


def persistentOutputWrapper(name):
    def wrapper(self, *args, **kwargs):
        res = getattr(self._data, name)(*args, **kwargs)
        inst = self.__class__()
        inst._data = res
        return inst
    return wrapper


def persistentOutputStrippingWrapper(name, can_reverse=False):
    def wrapper(self, other):
        if isinstance(other, self.__class__):
            other = other._data
        try:
            meth = getattr(self._data, name)
            arg = other
        except AttributeError:
            # See comments in the call to the outer function
            if not can_reverse:
                raise
            meth = getattr(other, name.replace('__r', '__', 1))
            arg = self._data

        res = meth(arg)
        inst = self.__class__()
        inst._data = res
        return inst
    return wrapper


def strippingWrapper(name):
    def wrapper(self, other):
        if isinstance(other, self.__class__):
            other = other._data
        return getattr(self._data, name)(other)
    return wrapper


class Set(persistent.Persistent):
    def __init__(self, iterable=()):
        self._data = set(iterable)

    __hash__ = None

    for nm in ('__cmp__', '__contains__', '__iter__', '__len__'):
        locals()[nm] = simpleWrapper(nm)

    for nm in ('__eq__', '__ge__', '__gt__', '__le__', '__lt__', '__ne__',
               'issubset', 'issuperset'):
        locals()[nm] = strippingWrapper(nm)

    for nm in ('difference', 'intersection', 'isdisjoint',
               'symmetric_difference', 'union'):
        locals()[nm] = persistentOutputWrapper(nm)

    for nm in (
            '__and__', '__rand__',
            '__or__', '__ror__',
            '__sub__', '__rsub__',
            '__xor__', '__rxor__',
    ):
        # The __rXXX__ methods are not required to be present on the ``set``
        # type by the language spec; the only documented requirements
        # are the non-reversed versions. Accordingly, PyPy < 7.3 doesn't
        # provide them.
        locals()[nm] = persistentOutputStrippingWrapper(
            nm,
            can_reverse=nm.startswith('__r') and not hasattr(set, nm))

    for nm in ('add', 'clear', 'difference_update', 'discard',
               'intersection_update', 'pop', 'remove',
               'symmetric_difference_update', 'update'):
        locals()[nm] = mutatingWrapper(nm)

    for nm in ('__iand__', '__ior__', '__isub__', '__ixor__'):
        locals()[nm] = mutatingStrippingWrapper(nm)

    def copy(self):
        return self.__class__(self._data)

    def __repr__(self):
        if sys.version_info < (3,):
            # set([1, 2, 3])
            items = repr(self._data)[5:-2]
        else:
            # {1, 2, 3}
            items = repr(self._data)[1:-1]
        return '%s.%s([%s])' % (
            self.__class__.__module__,
            self.__class__.__name__,
            items)
