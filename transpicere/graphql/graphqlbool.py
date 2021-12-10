from typing import Any
from graphql.type import GraphQLScalarType
from graphql.pyutils import inspect
from graphql.error import GraphQLError


def serialize(output_value: bool) -> int:
    return output_value


def parse(input_value: Any) -> int:
    try:
        # bool MUST be first: bool is instance of int
        if isinstance(input_value, bool):
            return input_value
        elif isinstance(input_value, int):
            if input_value == 0:
                return False
            elif input_value > 0:
                return True
        elif isinstance(input_value, float):
            if input_value.is_integer():
                return parse(int(input_value))
        elif isinstance(input_value, str):
            if input_value.lower() == 'true':
                return True
            elif input_value.lower() == 'false':
                return False
            else:
                return parse(int(input_value))
        raise ValueError(
            f"Bool cannot represent non integer value: {inspect(input_value)}")
    except ValueError:
        raise GraphQLError(
            f"Bool cannot represent non integer value: {inspect(input_value)}")


GraphQLBool = GraphQLScalarType(
    name="Bool",
    description="The `Bool` scalar type represents"
    " non-fractional signed whole numeric values.",
    serialize=serialize,
    parse_value=parse
)
