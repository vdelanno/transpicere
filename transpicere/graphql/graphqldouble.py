from decimal import Decimal, InvalidOperation
from typing import Any
from graphql.type import GraphQLScalarType
from graphql.pyutils import inspect
from graphql.error import GraphQLError


def serialize(output_value: float) -> float:
    return output_value


def parse(input_value: Any) -> float:
    try:
        # bool MUST be first: bool is instance of int
        return float(input_value)
    except (InvalidOperation, ValueError, TypeError):
        raise GraphQLError(
            f"Double cannot represent non decimal value: {inspect(input_value)}")


GraphQLDouble = GraphQLScalarType(
    name="Double",
    description="The `Double` scalar type represents"
    "floating point decimal signed numeric values.",
    serialize=serialize,
    parse_value=parse,
)
