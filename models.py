from mimetypes import init
from typing import List, Union, Dict, TypeVar, Type
from enum import Enum
from dataclasses import dataclass, field
from onnx import AttributeProto


T = TypeVar("T")


def from_obj_enum_to_str_enum(obj_enum, enum_class: Type[T]) -> T:
    for opt in enum_class:
        obj_enum_value = getattr(obj_enum, opt.name)
        if obj_enum_value == obj_enum:
            return getattr(enum_class, opt.name)
    raise RuntimeError("Enum not equal to obj enum class", obj_enum, enum_class)


@dataclass
class Base:
    __auto_filled_obj_field__ = []

    def from_obj(self: T, obj) -> T:
        for field in self.__class__.__auto_filled_obj_field__:
            setattr(self, field, getattr(obj, field))
        return self


@dataclass
class Attribute(Base):
    __auto_filled_obj_field__ = [
        "name",
        "description",
        "default_value",
        "required",
    ]

    class AttrType(str, Enum):
        FLOAT = "FLOAT"
        INT = "INT"
        STRING = "STRING"
        TENSOR = "TENSOR"
        GRAPH = "GRAPH"
        SPARSE_TENSOR = "SPARSE_TENSOR"
        TYPE_PROTO = "TYPE_PROTO"
        FLOATS = "FLOATS"
        INTS = "INTS"
        STRINGS = "STRINGS"
        TENSORS = "TENSORS"
        GRAPHS = "GRAPHS"
        SPARSE_TENSORS = "SPARSE_TENSORS"
        TYPE_PROTOS = "TYPE_PROTOS"

    name: str = ""
    description: str = ""
    type: AttrType = AttrType.FLOAT
    default_value: AttributeProto = field(default_factory=AttributeProto)
    required: bool = False

    def from_obj(self: T, obj) -> T:
        super().from_obj(obj)
        self.type = from_obj_enum_to_str_enum(obj.type, self.AttrType)
        return self


@dataclass
class FormalParameter(Base):
    __auto_filled_obj_field__ = [
        "name",
        "typeStr",
        "description",
        "isHomogeneous",
    ]

    class Option(str, Enum):
        Single = "Single"
        Optional = "Optional"
        Variadic = "Variadic"

    class DifferentiationCategory(str, Enum):
        Unknown = "Unknown"
        Differentiable = "Differentiable"
        NonDifferentiable = "NonDifferentiable"

    name: str = ""
    types: List[str] = field(default_factory=list)
    typeStr: str = ""
    description: str = ""
    option: Option = Option.Single
    isHomogeneous: bool = False
    differentiationCategory: DifferentiationCategory = DifferentiationCategory.Unknown

    def from_obj(self: T, obj) -> T:
        super().from_obj(obj)
        self.types = list(obj.types)
        self.option = from_obj_enum_to_str_enum(obj.option, self.Option)
        self.differentiationCategory = from_obj_enum_to_str_enum(
            obj.differentiationCategory, self.DifferentiationCategory
        )
        return self


@dataclass
class TypeConstraintParam(Base):
    __auto_filled_obj_field__ = [
        "type_param_str",
        "description",
    ]

    type_param_str: str = ""
    description: str = ""
    allowed_type_strs: List[str] = field(default_factory=list)

    def from_obj(self: T, obj) -> T:
        super().from_obj(obj)
        self.allowed_type_strs = list(obj.allowed_type_strs)
        return self


@dataclass
class Operator(Base):
    __auto_filled_obj_field__ = [
        "name",
        "domain",
        "support_level",
        "doc",
        "since_version",
        "deprecated",
        "min_input",
        "min_output",
    ]

    class SupportLevel(str, Enum):
        COMMON = "COMMON"
        EXPERIMENTAL = "EXPERIMENTAL"

    name: str = ""
    domain: str = ""
    support_level: SupportLevel = SupportLevel.COMMON
    doc: str = ""
    since_version: int = 0
    deprecated: bool = False
    min_input: int = 0
    max_input: Union[int, str] = 0
    min_output: int = 0
    max_output: Union[int, str] = 0
    attributes: Dict[str, Attribute] = field(default_factory=dict)
    inputs: List[FormalParameter] = field(default_factory=list)
    outputs: List[FormalParameter] = field(default_factory=list)
    type_constraints: List[TypeConstraintParam] = field(default_factory=list)

    def from_obj(self: T, obj) -> T:
        super().from_obj(obj)
        self.support_level = from_obj_enum_to_str_enum(
            obj.support_level, self.SupportLevel
        )
        for k, v in obj.attributes.items():
            self.attributes[k] = Attribute().from_obj(v)
        self.max_input = "infty" if obj.max_input > 1e6 else obj.max_input
        self.max_output = "infty" if obj.max_output > 1e6 else obj.max_output
        self.inputs = list(map(lambda x: FormalParameter().from_obj(x), obj.inputs))
        self.outputs = list(map(lambda x: FormalParameter().from_obj(x), obj.outputs))
        self.type_constraints = list(
            map(lambda x: TypeConstraintParam().from_obj(x), obj.type_constraints)
        )
        return self
