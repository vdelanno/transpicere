import pytest
from decimal import Decimal
from transpicere.graphql.graphqldecimal import parse, GraphQLDecimal, GraphQLError
from scalar_schema import check_scalar_schema
import sys


@ pytest.mark.parametrize("test_input", [
    "a",
    "1a",
    [1],
    {
        1: 0
    },
    str(print(sys.maxsize)) + '0'
])
def test_graphqldecimal_parse_error(test_input):
    with pytest.raises(GraphQLError):
        parse(test_input)


@ pytest.mark.parametrize("input_value, inner_value", [
    (0, Decimal(0)),
    (-10, Decimal(-10)),
    (10, Decimal(10)),
    (sys.maxsize, Decimal(sys.maxsize)),
    (0.0, Decimal(0)),
    (-10.0, Decimal(-10)),
    (10.0, Decimal(10)),
    (0.0, Decimal(0)),
    ("0", Decimal(0)),
    ("-10", Decimal(-10)),
    ("10", Decimal(10)),
    ("0.0", Decimal(0)),
    ("-10.0", Decimal(-10)),
    ("10", Decimal(10)),
    ("0.0", Decimal(0)),
    (1.5, Decimal(1.5)),
    ("1.5", Decimal(1.5)),
    (True, Decimal(1)),
    (False, Decimal(0)),
    (1, Decimal(1)),
    (1.0, Decimal(1)),
    (1.5, Decimal(1.5)),
    (sys.maxsize, Decimal(sys.maxsize)),
    ("1", Decimal(1)),
    ("1.0", Decimal(1))
])
def test_graphqldecimal_schema(input_value, inner_value):
    if isinstance(input_value, str):
        input_value = f'"{input_value}"'
    elif isinstance(input_value, bool):
        input_value = 'true' if input_value else 'false'
    check_scalar_schema(GraphQLDecimal, input_value, inner_value, inner_value)
