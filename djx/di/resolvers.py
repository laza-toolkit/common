import typing as t 

from collections.abc import Callable



from djx.common.utils import export, Void
from .inspect import BoundArguments

from .abc import Resolver, T_Injectable, T_Injector, T, T_Provider, T_Resolver
from . import abc

if not t.TYPE_CHECKING:
    __all__ = [
        'Resolver',
        'T_Resolver',
        'ResolverFactory',
    ]




if t.TYPE_CHECKING:
    from .. import Provider
    class ResolverFactory(Callable[[abc.Provider, t.Any], T_Resolver]):
        ...
else:
    ResolverFactory = Callable[[abc.Provider, t.Any], T_Resolver]

    


@export()
class ConcreteResolver(Resolver[T], t.Generic[T, T_Injectable]):

    __slots__ = 'concrete',

    concrete: T_Injectable

    def __init__(self, concrete: T_Injectable=None, value: T=Void, *, bound: T_Injector=None) -> None:
        super().__init__(value, bound=bound)
        self.concrete = concrete

    def clone(self, *args, **kwds):
        return super().clone(self.concrete, *args, **kwds)

    def __repr__(self) -> str: 
        bound, value = self.bound, self.value
        return f'{self.__class__.__name__}({self.concrete!r}, {bound=!s}, {value=!r})'
    



@export()
class ValueResolver(Resolver[T]):

    __slots__ = ()




@export()
class InjectorResolver(Resolver[T_Injector]):

    __slots__ = ()

    def __init__(self, value=Void, bound=None):
        self.value = self.bound = bound





                                                                                                                                                                 
@export()
class AliasResolver(ConcreteResolver[T, T_Injectable]):
    """Resolver Object"""

    __slots__ = 'params', 'cache', '__call__',

    alias: t.ClassVar[bool] = True

    def __init__(self, concrete, *, cache=False, params=None, **kwds):
        super().__init__(concrete, **kwds)
        self.cache = cache
        self.params = params
        if cache:
            def __call__(*a, **kw) -> T:
                if a or kw:
                    return self.bound.make(concrete, *a, **kw)
                val = self.value
                if val is Void:
                    val = self.value = self.bound.make(concrete)

                return val
                # self.value = self.bound.make(concrete, *a, **kw)
                # return self.value
        else:
            def __call__(*a, **kw) -> T:
                return self.bound.make(concrete, *a, **kw)
        self.__call__ = __call__

    def clone(self, *args, **kwds):
        kwds.setdefault('cache', self.cache)
        kwds.setdefault('params', self.params)
        return super().clone(*args, **kwds)

    def bind(self: T_Resolver, inj: T_Injector) -> T_Resolver:
        if not self.cache and self.params is None:
            return inj.content[self.concrete]
        else:
            return super().bind(inj)  


                                                                                                                                                             
@export()
class AliasWithParamsResolver(AliasResolver):
    """Resolver Object"""

    __slots__ = ()

    def __init__(self, concrete, *, cache=False, params=((), {}),  **kwds):
        super().__init__(concrete, **kwds)
        self.cache = cache
        self.params = params
        if cache:
            def __call__(*a, **kw) -> T:
                if a or kw:
                    _a, _kw = self.params
                    return self.bound.make(concrete, *_a, *a, **_kw, **kw)
                
                val = self.value
                if val is Void:
                    _a, _kw = self.params
                    val = self.value = self.bound.make(concrete, *_a, *a, **_kw, **kw)
                return val

                # _a, _kw = self.params
                # self.value = self.bound.make(concrete, *_a, *a, **_kw, **kw)
                # return self.value
        else:
            def __call__(*a, **kw) -> T:
                _a, _kw = self.params
                return self.bound.make(concrete, *_a, *a, **_kw, **kw)
        self.__call__ = __call__

    def clone(self, *args, **kwds):
        kwds.setdefault('cache', self.cache)
        return super().clone(*args, **kwds)




@export()
class FuncResolver(ConcreteResolver[T, Callable[..., T]]):
    """Resolver Object"""

    __slots__ = 'cache', '__call__'

    def __init__(self, concrete, *, cache=False, **kwds):
        super().__init__(concrete, **kwds)
        self.cache = cache
        if cache:
            def __call__(*args, **kwds) -> T:
                if args or kwds:
                    return concrete(*args, **kwds)
                
                val = self.value
                if val is Void:
                    val = self.value = concrete()
                return val

            self.__call__ = __call__
        else:
            self.__call__ = concrete

    def clone(self, *args, **kwds):
        kwds.setdefault('cache', self.cache)
        return super().clone(*args, **kwds)





@export()
class FuncParamsResolver(FuncResolver):
    """FuncParamsResolver Object"""

    __slots__ = 'params',

    params: BoundArguments

    def __init__(self, concrete, *, params=None, **kwds):
        super().__init__(concrete, **kwds)

        self.params = params
        if self.cache:
            def __call__(*args, **kwds) -> T:
                if args or kwds:
                    bound = self.bound
                    return concrete(*params.inject_args(bound, kwds), *args, **params.inject_kwargs(bound, kwds))

                val = self.value
                if val is Void:
                    bound = self.bound
                    self.value = val = concrete(*params.inject_args(bound), **params.inject_kwargs(bound))

                return val
        else:
            def __call__(*args, **kwds) -> T:
                bound = self.bound
                return concrete(*params.inject_args(bound, kwds), *args, **params.inject_kwargs(bound, kwds))
                
        self.__call__ = __call__
    
    def clone(self, *args, **kwds):
        kwds.setdefault('params', self.params)
        return super().clone(*args, **kwds)

