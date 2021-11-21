import pytest
from decimal import Decimal
from transpicere.graphql.graphqldecimal import parse, GraphQLDecimal, GraphQLError
from scalar_schema import check_scalar_schema
import sys


# @ pytest.mark.parametrize("test_input", [
# ])
# def test_graphqldecimal_parse_error(test_input):
#     with pytest.raises(GraphQLError):
#         parse(test_input)


@ pytest.mark.parametrize("input_value, inner_value, expect_error", [
    (0, Decimal(0), False),
    (-10, Decimal(-10), False),
    (10, Decimal(10), False),
    (sys.maxsize, Decimal(sys.maxsize), False),
    (0.0, Decimal(0), False),
    (-10.0, Decimal(-10), False),
    (10.0, Decimal(10), False),
    (0.0, Decimal(0), False),
    ("0", Decimal(0), False),
    ("-10", Decimal(-10), False),
    ("10", Decimal(10), False),
    ("0.0", Decimal(0), False),
    ("-10.0", Decimal(-10), False),
    ("10", Decimal(10), False),
    ("0.0", Decimal(0), False),
    (1.5, Decimal(1.5), False),
    ("1.5", Decimal(1.5), False),
    (True, Decimal(1), False),
    (False, Decimal(0), False),
    (1, Decimal(1), False),
    (1.0, Decimal(1), False),
    (1.5, Decimal(1.5), False),
    (f"{sys.maxsize}", Decimal(sys.maxsize), False),
    ("1", Decimal(1), False),
    ("1.0", Decimal(1), False),
    # failures
    ("a", None, True),
    ("1a", None, True),
    ([1], None, True),
    ({
        1: 0
    }, None, True),
    (str(print(sys.maxsize)) + '0', None, True),
])
def test_graphqldecimal_schema(input_value, inner_value, expect_error):
    if isinstance(input_value, str):
        input_value = f'"{input_value}"'
    elif isinstance(input_value, bool):
        input_value = 'true' if input_value else 'false'
    check_scalar_schema(GraphQLDecimal, input_value,
                        inner_value, inner_value, expect_error)
