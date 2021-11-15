from decimal import Decimal, InvalidOperation
from typing import Any
from graphql.language.ast import ValueNode
from graphql.type import GraphQLScalarType
from graphql.pyutils import inspect
from graphql.language.ast import (
    BooleanValueNode,
    FloatValueNode,
    IntValueNode,
    StringValueNode,
    ValueNode,
)
from graphql.error import GraphQLError
from graphql.language.printer import print_ast


def serialize(output_value: Decimal) -> Decimal:
    return output_value


def parse(input_value: Any) -> Decimal:
    try:
        # bool MUST be first: bool is instance of int
        return Decimal(input_value)
    except (InvalidOperation, ValueError, TypeError):
        raise GraphQLError(
            f"Decimal cannot represent non decimal value: {inspect(input_value)}")


def parse_literal(value_node: ValueNode, _variables: Any = None) -> Decimal:
    if isinstance(value_node, IntValueNode):
        return parse(int(value_node.value))
    elif isinstance(value_node, FloatValueNode):
        return parse(value_node.value)
    elif isinstance(value_node, BooleanValueNode):
        return parse(bool(value_node.value))
    elif isinstance(value_node, StringValueNode):
        return parse(value_node.value)
    raise GraphQLError(
        f"Decimal cannot represent non decimal value: {print_ast(value_node)}", value_node)


GraphQLDecimal = GraphQLScalarType(
    name="Decimal",
    description="The `Decimal` scalar type represents"
    " exact decimal signed numeric values.",
    serialize=serialize,
    parse_value=parse,
    parse_literal=parse_literal,
)
