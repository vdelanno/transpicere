import pytest
from transpicere.graphql.graphqllong import parse, GraphQLLong, GraphQLError
from scalar_schema import check_scalar_schema
import sys


@pytest.mark.parametrize("test_input", [
    "a",
    "1a",
    1.5,
    "1.5",
    [1],
    {
        1: 0
    },
    str(print(sys.maxsize)) + '0'
])
def test_graphqllong_parse_error(test_input):
    with pytest.raises(GraphQLError):
        parse(test_input)


@pytest.mark.parametrize("input_value, inner_value", [
    (0, 0),
    (-10, -10),
    (10, 10),
    (sys.maxsize, sys.maxsize),
    (0.0, 0),
    (-10.0, -10),
    (10.0, 10),
    (0.0, 0),
    ('"0"', 0),
    ('"-10"', -10),
    ('"10"', 10),
    ('"0.0"', 0),
    ('"-10.0"', -10),
    ('"10"', 10),
    ('"0.0"', 0),
    (1, 1),
    (1.0, 1),
    (sys.maxsize, sys.maxsize),
    ("true", 1),
    ("false", 0),
    ('"1"', 1),
    ('"1.0"', 1)
])
def test_graphqllong_schema(input_value, inner_value):
    check_scalar_schema(GraphQLLong, input_value, inner_value, inner_value)
