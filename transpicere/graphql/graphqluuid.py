import uuid
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


def serialize(output_value: uuid.UUID) -> uuid.UUID:
    return output_value


def parse(input_value: Any) -> uuid.UUID:
    try:
        if isinstance(input_value, str):
            return uuid.UUID(input_value)
    except (ValueError, TypeError):
        pass
    raise GraphQLError(
        f"Uuid cannot represent non decimal value: {inspect(input_value)}")


def parse_literal(value_node: ValueNode, _variables: Any = None) -> uuid.UUID:
    if isinstance(value_node, StringValueNode):
        return parse(value_node.value)
    raise GraphQLError(
        f"Decimal cannot represent non decimal value: {print_ast(value_node)}", value_node)


GraphQLUuid = GraphQLScalarType(
    name="UUID",
    description="The `UUID` scalar type represents"
    " a uuid.",
    serialize=serialize,
    parse_value=parse,
    parse_literal=parse_literal,
)
