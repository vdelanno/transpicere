from enum import Enum


class BaseType(Enum):
    Bool = 'bool'
    Long = 'long'
    Float = 'float'
    String = 'string'
    Decimal = 'decimal'
    Date = 'date'
    Time = 'time'
    Datetime = 'datetime'
    Uuid = 'uuid'
