from abc import ABC
from typing import Dict, Type, Generic, TypeVar, ClassVar, List, Optional

from dataclasses import fields, dataclass, Field
from typing_inspect import is_optional_type, get_args, is_forward_ref

T = TypeVar('T')
SelfT = TypeVar('SelfT')

KIND_FIELD_NAME = 'kind_name'


@dataclass
class _TaggedUnionStruct(Generic[T]):
    field_types: Dict[str, Type[T]]
    field_names: Dict[Type[T], str]

    @classmethod
    def from_fields(cls, fields: List[Field]):
        used_types = []
        field_types: Dict[str, Type[T]] = {}
        field_names: Dict[Type[T], str] = {}

        kind_field, *fields = fields

        if not (kind_field.name == KIND_FIELD_NAME and kind_field.type == Optional[str]):
            raise ValueError('invalid `%s` field type: (%s)' % (KIND_FIELD_NAME, kind_field,))

        invalid_fields = []
        for field in fields:
            field_type = field.type

            if not is_optional_type(field_type):
                invalid_fields.append((field, 'field must be Optional'))
                continue

            optional_type, _ = get_args(field_type)

            relatives = [x for x in used_types if issubclass(optional_type, x) or issubclass(x, optional_type)]

            if any(relatives):
                raise ValueError('`%s` is relative of `%s`' % (optional_type, relatives))

            if is_forward_ref(optional_type):
                raise ValueError('forward references are not supported: can\'t use \'\' around types')

            used_types.append(optional_type)

            field_types[field.name] = optional_type
            field_names[optional_type] = field.name

        if len(invalid_fields):
            raise TypeError('unsupported fields found: %s' % ([(f.name, err) for f, err in invalid_fields],))

        return _TaggedUnionStruct(
            field_names=field_names,
            field_types=field_types,
        )


MISSING = object()


@dataclass
class TaggedUnion(ABC, Generic[T]):
    """
    a good-enough implementation of a tagged union backed by a dataclass

    does _not_ support forward type references (but to support it, look at ``typing.ForwardRef._evaluate``)
    """

    kind_name: Optional[str] = MISSING
    _field_types: ClassVar[Dict[str, Type[T]]]
    _field_names: ClassVar[Dict[Type[T], str]]
    _superclass: ClassVar[Type[T]]

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if cls.__name__ == TaggedUnion.__name__:
            # todo could not extract the generic type information
            pass
        else:
            rt = _TaggedUnionStruct.from_fields(list(fields(dataclass(cls))))

            cls._field_types = rt.field_types
            cls._field_names = rt.field_names

    def __post_init__(self):
        values = [n for n in self._field_types.keys() if getattr(self, n) is not None]

        if len(values) != 1:
            raise ValueError('tagged union only supports one value at a time (%s)' % (values,))

        kind, = values

        if self.kind_name is MISSING:
            self.kind_name = kind
        elif kind != self.kind_name:
            raise ValueError('tagged union `kind_name` is incorrectly set up (%s)' % (kind,))

    @classmethod
    def field_name(cls: 'Type[TaggedUnion[T]]', val: T) -> str:
        rtn = cls._field_names.get(val.__class__)

        if rtn is None:
            raise ValueError('not a member of tagged union')

        return rtn

    @classmethod
    def from_value(
            cls: Type[SelfT],
            val: T,
    ) -> SelfT:
        kind = cls.field_name(val)

        return cls(**{
            KIND_FIELD_NAME: kind,
            kind: val,
        })

    @property
    def kind(self) -> Type[T]:
        return self._field_types[self.kind_name]

    def value(self) -> T:
        return getattr(self, self.kind_name)
