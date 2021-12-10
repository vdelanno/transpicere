import pytest
from transpicere.graphql.graphqlbool import parse, GraphQLBool, GraphQLError
from scalar_schema import check_scalar_schema
import sys


@pytest.mark.parametrize("input_value, inner_value, expect_error", [
    (0, False, False),
    (1, True, False),
    ('true', True, False),
    ('false', False, False),
    ('"true"', True, False),
    ('"false"', False, False),
    (1.0, True, False),
    (0.0, False, False),
    (2, True, False),
    ('"1"', True, False),
    ('"0"', False, False),
    (str(sys.maxsize) + '0', True, False),
    # failures
    (-1, None, True),
    ("a", None, True),
    ("1a", None, True),
    (1.5, None, True),
    ("1.5", None, True),
    ([1], None, True),
    ({
        1: 0
    }, None, True),
])
def test_graphqlbool_schema(input_value, inner_value, expect_error):
    check_scalar_schema(GraphQLBool, input_value,
                        inner_value, inner_value, expect_error)
