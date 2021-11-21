import uuid
from typing import Any
from graphql.type import GraphQLScalarType
from graphql.pyutils import inspect
from graphql.error import GraphQLError


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


GraphQLUuid = GraphQLScalarType(
    name="UUID",
    description="The `UUID` scalar type represents"
    " a uuid.",
    serialize=serialize,
    parse_value=parse
)
