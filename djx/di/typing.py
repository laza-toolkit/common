
from abc import ABC, abstractmethod
import typing as t 

from functools import partial

from djx.common import typing as tt
from djx.common.utils import export




@export()
def get_args(tp):
    return tt.get_args(tp)


@export()
def get_origin(obj):
    if isinstance(obj, InjectableForm):
        return obj.__injectable_origin__
    return tt.get_origin(obj)


@export()
def get_all_type_hints(obj: t.Any, globalns: t.Any = None, localns: t.Any = None) -> t.Any:
    return tt.get_all_type_hints(obj, globalns=globalns, localns=localns)


class InjectableForm(ABC):

    __slots__ = ()

    @property
    @abstractmethod
    def __injectable_origin__(self):
        ...

    def __call__(self):
        raise TypeError(f"Type {self!r} cannot be instantiated.")
