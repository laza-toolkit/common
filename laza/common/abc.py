from abc import abstractmethod
import typing as t 

from collections.abc import Iterable

from .functools import export

abstractmethod

_T_Abc = t.TypeVar('_T_Abc', bound=type, covariant=True)


def abstractclass(klass: _T_Abc=None) -> _T_Abc:
    """A decorator indicating abstract class.
    
    Abstract classes cannot be instantiated. However subclasses that are not 
    abstract can. 

    Works by setting the class's `__abstractmethods__` to given `abstract`
    """

    def decorator(cls: _T_Abc) -> _T_Abc:
        if not getattr(cls, '__abstractmethods__', None):
            cls.__abstractmethods__ = frozenset(['__name__'])
        return cls

    return decorator if klass is None else decorator(klass)


@export()
class Representation:
    """
    Mixin to provide __str__, __repr__, and __pretty__ methods. See #884 for more details.

    __pretty__ is used by [devtools](https://python-devtools.helpmanual.io/) to provide human readable representations
    of objects.
    """

    __slots__: tuple[str, ...] = ()

    def __repr_args__(self):
        """
        Returns the attributes to show in __str__, __repr__, and __pretty__ this is generally overridden.

        Can either return:
        * name - value pairs, e.g.: `[('foo_name', 'foo'), ('bar_name', ['b', 'a', 'r'])]`
        * or, just values, e.g.: `[(None, 'foo'), (None, ['b', 'a', 'r'])]`
        """
        attrs = ((s, getattr(self, s)) for s in self.__slots__)
        return [(a, v) for a, v in attrs if v is not None]

    def __repr_name__(self) -> str:
        """
        Name of the instance's class, used in __repr__.
        """
        return self.__class__.__name__

    def __repr_str__(self, join_str: str) -> str:
        return join_str.join(repr(v) if a is None else f'{a}={v!r}' for a, v in self.__repr_args__())

    def __pretty__(self, fmt, **kwargs) -> t.Generator[t.Any, None, None]:
        yield self.__repr_name__() + '('
        yield 1
        for name, value in self.__repr_args__():
            if name is not None:
                yield name + '='
            yield fmt(value)
            yield ','
            yield 0
        yield -1
        yield ')'

    def __str__(self) -> str:
        return self.__repr_str__(' ')

    def __repr__(self) -> str:
        return f'{self.__repr_name__()}({self.__repr_str__(", ")})'




# @export()
# class Fluent(ABCMeta):
#     """
#     """
#     __slots__ = ()

#     def __getattr__(self, key):
#         return None 



# @export()
# class FluentMapping(Mapping):
#     __slots__ = ()

#     @abstractmethod
#     def __missing__(self, key):
#         return None 


    


# def _check_methods(C, *methods):
#     mro = C.__mro__
#     for method in methods:
#         for B in mro:
#             if method in B.__dict__:
#                 if B.__dict__[method] is None:
#                     return NotImplemented
#                 break
#         else:
#             return NotImplemented
#     return True



# @export()
# class Orderable(metaclass=ABCMeta):
#     """SupportsOrdering Object"""
#     __slots__ = ()
    
#     def __order__(self):
#         return self

#     def __eq__(self, it, orderby=None) -> bool:
#         if isinstance(it, Orderable):
#             return it == (orderby or self.__class__.__order__)(self)
#         return NotImplemented

#     def __ne__(self, it, orderby=None) -> bool:
#         return not self.__eq__(it, orderby)

#     def __gt__(self, it, orderby=None) -> bool:
#         if isinstance(it, Orderable):
#             return (orderby or self.__class__.__order__)(self) > it
#         return NotImplemented

#     def __ge__(self, it, orderby=None) -> bool:
#         return it is self or self.__gt__(it, orderby) or self.__eq__(it, orderby)

#     def __lt__(self, it, orderby=None) -> bool:
#         if isinstance(it, Orderable):
#             return (orderby or self.__class__.__order__)(self) < it
#         return NotImplemented

#     def __le__(self, it, orderby=None) -> bool:
#         return it is self or self.__lt__(it, orderby) or self.__eq__(it, orderby)

#     @classmethod
#     def __subclasshook__(cls, subclass: type) -> bool:
#         if cls is Orderable:
#             return _check_methods(subclass, '__eq__', '__ge__', '__gt__', '__le__', '__lt__')
#         return NotImplemented



# Orderable.register(str)
# Orderable.register(int)
# Orderable.register(float)
# Orderable.register(bytes)
# Orderable.register(tuple)
# Orderable.register(Set)
# Orderable.register(frozenset)
# Orderable.register(set)



# @export()
# class Immutable(metaclass=ABCMeta):
#     """SupportsOrdering Object"""
#     __slots__ = ()

#     __mutable__: t.ClassVar[t.Union[type[t.Any], tuple[type[t.Any]]]] = ...
#     __immutable__: t.ClassVar[t.Union[type[t.Any], tuple[type[t.Any]]]] = ...
    
#     def __init_subclass__(cls, *, mutable=..., immutable=...) -> None:
#         if mutable is not ...:
#             cls.__mutable__ = mutable
#         if immutable is not ...:
#             cls.__immutable__ = immutable
        

#     @classmethod
#     def __subclasshook__(cls, sub: type) -> bool:
#         if Immutable in cls.__bases__ and cls.__mutable__ and cls.__immutable__:
#             return issubclass(sub, cls.__immutable__) and not issubclass(sub, cls.__mutable__)
#         return NotImplemented


# @export()
# class ImmutableSequence(Immutable, immutable=Sequence, mutable=MutableSequence):

#     __slots__ = ()


# @export()
# class ImmutableSet(Immutable, immutable=Set, mutable=MutableSet):

#     __slots__ = ()


# @export()
# class ImmutableMapping(Immutable, immutable=Mapping, mutable=MutableMapping):

#     __slots__ = ()


