from decimal import Decimal, InvalidOperation
from typing import Any
from graphql.type import GraphQLScalarType
from graphql.pyutils import inspect
from graphql.error import GraphQLError


def serialize(output_value: Decimal) -> Decimal:
    return output_value


def parse(input_value: Any) -> Decimal:
    try:
        # bool MUST be first: bool is instance of int
        return Decimal(input_value)
    except (InvalidOperation, ValueError, TypeError):
        raise GraphQLError(
            f"Decimal cannot represent non decimal value: {inspect(input_value)}")


GraphQLDecimal = GraphQLScalarType(
    name="Decimal",
    description="The `Decimal` scalar type represents"
    " exact decimal signed numeric values.",
    serialize=serialize,
    parse_value=parse,
)
