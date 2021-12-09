import pytest
from transpicere.graphql.graphqldouble import parse, GraphQLDouble, GraphQLError
from scalar_schema import check_scalar_schema
import sys


@pytest.mark.parametrize("input_value, inner_value, expect_error", [
    (0, 0.0, False),
    (-10, -10.0, False),
    (10, 10.0, False),
    (0.0, 0.0, False),
    (-10.0, -10.0, False),
    (10.0, 10.0, False),
    (0.0, 0.0, False),
    ('"0"', 0.0, False),
    ('"-10"', -10.0, False),
    ('"10"', 10.0, False),
    ('"0.0"', 0.0, False),
    ('"-10.0"', -10.0, False),
    ('"10"', 10.0, False),
    ('"0.0"', 0.0, False),
    (1, 1.0, False),
    (1.0, 1.0, False),
    ('"1"', 1.0, False),
    ('"1.0"', 1.0, False),
    (1.5, 1.5, False),
    ("1.5", 1.5, False),
    ('"1.0005"', 1.0005, False),
    ('".0005"', .0005, False),
    # failures
    ("true", None, True),
    ("false", None, True),
    ("a", None, True),
    ("1a", None, True),
    ([1], None, True),
    ({
        1: 0
    }, None, True),
    (str(print(sys.maxsize)) + '0', None, True),
])
def test_graphqldouble_schema(input_value, inner_value, expect_error):
    print(f"{input_value}, {inner_value}, {expect_error}")
    check_scalar_schema(GraphQLDouble, input_value,
                        inner_value, inner_value, expect_error)
