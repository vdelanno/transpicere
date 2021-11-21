import pytest
from transpicere.graphql.graphqluuid import parse, GraphQLUuid, GraphQLError
from scalar_schema import check_scalar_schema
import sys
from uuid import UUID


@pytest.mark.parametrize("test_input", [
    '"1234567812345678123456781234567"',
    "a",
    [1],
    {
        1: 2
    }

])
def test_graphqllong_parse_error(test_input):
    with pytest.raises(GraphQLError):
        parse(test_input)


TEST_UUID = UUID("12345678-1234-5678-1234-567812345678")


@pytest.mark.parametrize("input_value, inner_value, expect_error", [
    ('"{12345678-1234-5678-1234-567812345678}"', TEST_UUID, False),
    ('"12345678-1234-5678-1234-567812345678"', TEST_UUID, False),
    ('"12345678123456781234567812345678"', TEST_UUID, False),
    ('"urn:uuid:12345678123456781234567812345678"', TEST_UUID, False),
])
def test_graphqllong_schema(input_value, inner_value, expect_error):
    check_scalar_schema(GraphQLUuid, input_value,
                        inner_value, inner_value, expect_error)
