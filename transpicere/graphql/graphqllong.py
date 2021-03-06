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


def serialize(output_value: int) -> int:
    return output_value


def parse(input_value: Any) -> int:
    try:
        # bool MUST be first: bool is instance of int
        if isinstance(input_value, bool):
            return 1 if input_value else 0
        elif isinstance(input_value, int):
            return input_value
        elif isinstance(input_value, float):
            if input_value.is_integer():
                return int(input_value)
        elif isinstance(input_value, str):
            comma_index = input_value.find('.')
            if comma_index != -1:
                if input_value[comma_index+1:] == '0'*(len(input_value) - comma_index - 1):
                    return int(input_value[0:comma_index])
            else:
                return int(input_value)
        raise ValueError(
            f"Long cannot represent non integer value: {inspect(input_value)}")
    except ValueError:
        raise GraphQLError(
            f"Long cannot represent non integer value: {inspect(input_value)}")


def parse_literal(value_node: ValueNode, _variables: Any = None) -> int:
    if isinstance(value_node, IntValueNode):
        return parse(int(value_node.value))
    elif isinstance(value_node, FloatValueNode):
        return parse(float(value_node.value))
    elif isinstance(value_node, BooleanValueNode):
        return parse(bool(value_node.value))
    elif isinstance(value_node, StringValueNode):
        return parse(value_node.value)
    raise GraphQLError(
        f"Long cannot represent non integer value: {print_ast(value_node)}", value_node)


GraphQLLong = GraphQLScalarType(
    name="Long",
    description="The `Long` scalar type represents"
    " non-fractional signed whole numeric values.",
    serialize=serialize,
    parse_value=parse,
    parse_literal=parse_literal,
)
