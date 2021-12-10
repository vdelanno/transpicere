import pytest
from transpicere.graphql.graphqllong import parse, GraphQLLong, GraphQLError
from scalar_schema import check_scalar_schema
import sys


@pytest.mark.parametrize("input_value, inner_value, expect_error", [
    (0, 0, False),
    (-10, -10, False),
    (10, 10, False),
    (sys.maxsize, sys.maxsize, False),
    (0.0, 0, False),
    (-10.0, -10, False),
    (10.0, 10, False),
    (0.0, 0, False),
    ('"0"', 0, False),
    ('"-10"', -10, False),
    ('"10"', 10, False),
    ('"0.0"', 0, False),
    ('"-10.0"', -10, False),
    ('"10"', 10, False),
    ('"0.0"', 0, False),
    (1, 1, False),
    (1.0, 1, False),
    (f"{sys.maxsize}", sys.maxsize, False),
    ("true", 1, False),
    ("false", 0, False),
    ('"1"', 1, False),
    ('"1.0"', 1, False),
    (str(sys.maxsize) + '0', 92233720368547758070, False),
    # failures
    ("a", None, True),
    ("1a", None, True),
    (1.5, None, True),
    ("1.5", None, True),
    ([1], None, True),
    ({
        1: 0
    }, None, True),
])
def test_graphqllong_schema(input_value, inner_value, expect_error):
    check_scalar_schema(GraphQLLong, input_value,
                        inner_value, inner_value, expect_error)
