from inspect import Signature
import mimetypes
from abc import ABC, abstractmethod
import typing
from typing import Union, Dict, List, Any, AnyStr, Text, Type

from marshmallow import Schema, fields


class ResponseObjectInterface(ABC):
    """
    Abstract Response Class.  Extend to create custom response types that can be handled by AutoMD
    """
    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @staticmethod
    @abstractmethod
    def to_schema() -> Schema:
        pass

    @staticmethod
    @abstractmethod
    def content_type() -> str:
        pass


class ValueResponse(ResponseObjectInterface):
    class ValueResponseSchema(Schema):
        value = fields.Field(required=True,
                             validate=(lambda x: type(x) in [int, float, str, bool, dict, list]),
                             description=("General value field, can hold an"
                                          " Integer, Float, String, Boolean, Dictionary, or List"))

    def __init__(self, value: Union[float, int, str, bool, List, Dict]):
        """
        "General value response, can hold an Integer, Float, String, Boolean, Dictionary, or List"
        :param value:
        """
        super().__init__()
        self.value: Union[float, int, str, bool, List, Dict] = value

    def to_dict(self) -> Dict:
        """
        Return a representation of the Response Object as a dictionary for json serialization
        :return:
        """
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema() -> Schema:
        """
        Return a Schema representation of the Response Object
        :return:
        """
        return ValueResponse.ValueResponseSchema()

    @staticmethod
    def content_type() -> str:
        """
        Return the Content Type for the Response Object for HTTP serialization
        :return:
        """
        return mimetypes.MimeTypes().types_map[1][".json"]


class ListResponse(ResponseObjectInterface):
    class ListResponseSchema(Schema):
        value = fields.List(fields.Raw(), required=True, description="List response field")

    def __init__(self, value: List):
        """
        "List Response"
        :param value:
        """
        super().__init__()
        self.value: List = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema() -> Schema:
        return ListResponse.ListResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1][".txt"]


class DictResponse(ResponseObjectInterface):
    class DictResponseSchema(Schema):
        # TODO make this value, or make all the other response, and reconcile with to_dict
        response = fields.Dict(required=True, description="Object response field")

    def __init__(self, value: Dict):
        """
        Dictionary response field
        :param value:
        """
        super().__init__()
        self.value: Dict = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema() -> Schema:
        return DictResponse.DictResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1][".json"]


class JSONResponse(ResponseObjectInterface):
    class JSONResponseSchema(Schema):
        # TODO introduce Polymorphic Field
        value = fields.Field(required=True,
                             validate=(lambda x: type(x) in [dict, list]),
                             description="JSON response field")

    def __init__(self, value: Union[List, Dict]):
        """
        "JSON response field"
        :param value:
        """
        super().__init__()
        self.value: Union[List, Dict] = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema() -> Schema:
        return JSONResponse.JSONResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1][".json"]


class StringResponse(ResponseObjectInterface):
    class StringResponseSchema(Schema):
        value = fields.String(required=True, description="String response field")

    def __init__(self, value: str):
        """
        String response field
        :param value:
        """
        super().__init__()
        self.value: str = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema() -> Schema:
        return StringResponse.StringResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1][".txt"]


class IntegerResponse(ResponseObjectInterface):
    class IntegerResponseSchema(Schema):
        value = fields.Integer(required=True, description="Integer response field")

    def __init__(self, value: int):
        """
        "Integer response field"
        :param value:
        """
        super().__init__()
        self.value: int = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema() -> Schema:
        return IntegerResponse.IntegerResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1][".txt"]


class FloatResponse(ResponseObjectInterface):
    class FloatResponseSchema(Schema):
        value = fields.Float(required=True, description="Float response field")

    def __init__(self, value: float):
        """
        "Float response field"
        :param value:
        """
        super().__init__()
        self.value: float = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema() -> Schema:
        return FloatResponse.FloatResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1][".txt"]


response_object_type_map: Dict[Any, Type[ResponseObjectInterface]] = {
    int: IntegerResponse,
    "int": IntegerResponse,
    float: FloatResponse,
    "float": FloatResponse,
    str: StringResponse,
    "str": StringResponse,
    list: ListResponse,
    "list": ListResponse,
    List: ListResponse,
    getattr(List, "_name", "List._name"): ListResponse,
    getattr(List, "_gorg", "List._gorg"): ListResponse,
    "List": ListResponse,
    dict: DictResponse,
    "dict": DictResponse,
    Dict: DictResponse,
    getattr(Dict, "_name", "Dict._name"): DictResponse,
    getattr(Dict, "_gorg", "Dict._gorg"): DictResponse,
    "Dict": DictResponse,
    Signature.empty: None,
    Any: ValueResponse,
    getattr(Any, "_name", "Any._name"): ValueResponse,
    getattr(Any, "_gorg", "Any._gorg"): ValueResponse,
    "Any": ValueResponse
}


def map_response_object_type(key: Any,
                             default: Union[ResponseObjectInterface, Type[ResponseObjectInterface]] = None
                             ) -> Type[ResponseObjectInterface]:
    ret_interface: Type[ResponseObjectInterface] = response_object_type_map.get(key)

    if ret_interface is None:
        name: str = getattr(key, "_name", getattr(key, "_gorg", None))
        ret_interface = response_object_type_map.get(name)

    return ret_interface or default


type_field_mapping: Dict[Any, Type[fields.Field]] = {
    bool: fields.Boolean,
    "bool": fields.Boolean,
    int: fields.Integer,
    "int": fields.Integer,
    float: fields.Float,
    "float": fields.Float,
    str: fields.String,
    "str": fields.String,
    Text: fields.String,
    AnyStr: fields.String,
    dict: fields.Dict,
    "dict": fields.Dict,
    "Dict": fields.Dict,
    Dict: fields.Dict,
    getattr(Dict, "_name", "Dict._name"): fields.Dict,
    getattr(Dict, "_gorg", "Dict._gorg"): fields.Dict,
    list: fields.List,
    "list": fields.List,
    "List": fields.List,
    List: fields.List,
    getattr(List, "_name", "List._name"): fields.List,
    getattr(List, "_gorg", "List._gorg"): fields.List,
    Any: fields.Raw,
    "Any": fields.Raw,
    getattr(Any, "_name", "Any._name"): fields.Raw,
    getattr(Any, "_gorg", "Any._gorg"): fields.Raw,
    Signature.empty: fields.Raw,
}


def map_type_field_mapping(key: Any,
                           default: fields.Field = None) -> Type[fields.Field]:
    ret_field: Type[fields.Field] = type_field_mapping.get(key)

    if ret_field is None:
        name: str = getattr(key, "_name", getattr(key, "_gorg", None))
        ret_field = type_field_mapping.get(name)

    return ret_field or default


def type_to_field(key: Any, default: fields.Field = None, **kwargs) -> fields.Field:
    field_class: Type[fields.Field] = map_type_field_mapping(key, default)

    field_args: List = []
    if field_class == fields.List:
        list_field: fields.Field = fields.Raw()
        try:
            list_field: fields.Field = map_type_field_mapping(typing.get_args(key)[0])()
        except:
            try:
                list_field: fields.Field = map_type_field_mapping(key.__args__[0])()
            except:
                pass

        field_args.append(list_field)
    elif field_class == fields.Dict:
        key_field: fields.Field = fields.Raw()
        value_field: fields.Field = fields.Raw()

        try:  # Try Python 3.8 method
            key_field: fields.Field = map_type_field_mapping(typing.get_args(key)[0])()
            value_field: fields.Field = map_type_field_mapping(typing.get_args(key)[1])()
        except:
            try:  # Then try Python 3.6/3.7
                key_field: fields.Field = map_type_field_mapping(key.__args__[0])()
                value_field: fields.Field = map_type_field_mapping(key.__args__[1])()
            except:
                pass

        kwargs["keys"] = key_field
        kwargs["values"] = value_field

    return field_class(*field_args, **kwargs)
