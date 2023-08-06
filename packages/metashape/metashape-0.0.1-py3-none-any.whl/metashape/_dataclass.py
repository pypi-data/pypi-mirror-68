import typing as t
import sys
from collections import ChainMap
from dataclasses import fields, Field
from dataclasses import is_dataclass
from .types import MetaData, IteratePropsFunc


def iterate_props(
    typ: t.Type[t.Any], *, ignore_private: bool = True
) -> t.Iterable[t.Tuple[str, t.Type[t.Any], t.Optional[MetaData]]]:
    for field in fields(typ):  # type: Field[t.Any]
        mutable_state: t.Dict[str, t.Any] = {}
        metadata = ChainMap(mutable_state, field.metadata)
        field_type = _evaluate_type(typ, field)
        yield field.name, field_type, metadata


def _evaluate_type(
    typ: t.Type[t.Any], field: "Field[t.Any]", *, _empty: t.Dict[str, t.Any] = {}
) -> t.Type[t.Any]:
    field_type = field.type
    if not isinstance(field_type, str):
        return field_type
    m = sys.modules[typ.__module__]
    field_type = field.type = t.ForwardRef(field_type)._evaluate(m.__dict__, _empty)
    return field_type


# type assertion
_: IteratePropsFunc = iterate_props

__all__ = ["iterate_props", "is_dataclass", "Field", "fields"]
