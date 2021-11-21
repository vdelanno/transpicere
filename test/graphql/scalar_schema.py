from graphql import GraphQLObjectType, GraphQLField, GraphQLArgument, GraphQLSchema, graphql_sync
from functools import partial


def resolve_inner_value(inner_value, root, _info, value):
    print(f"inner_value {inner_value} {type(inner_value)}")
    print(f"value {value} {type(value)}")
    assert type(inner_value) == type(
        value), f"value {value}({type(value)}) is not of expected type {type(inner_value)} is not of type"
    assert inner_value == value, f"value {value}({type(value)}) is not of expected value {inner_value}"
    return {
        'value': inner_value
    }


def check_scalar_schema(scalar_type, input_value, inner_value, output_value, expect_errors):
    scalar_object_type = GraphQLObjectType('Scalar', {
        'value': GraphQLField(
            scalar_type,
            description='test value.')
    },
        description='A scalar test.'
    )

    query_type = GraphQLObjectType('Query', lambda: {
        'get': GraphQLField(scalar_object_type, args={
            'value': GraphQLArgument(
                scalar_type,
                description='input test value')},
            resolve=partial(resolve_inner_value, inner_value)),
    })
    schema = GraphQLSchema(query_type)
    query = f"""
    {{
        get(value: {input_value}) {{
            value
        }}
    }}
    """
    print(f"query: {query}")
    result = graphql_sync(schema, query)
    print(f"result: {result}")
    if expect_errors:
        assert result.errors is not None
        assert len(result.errors) == 1
    else:
        assert result.errors is None or len(result.errors) == 0
        assert result.data['get']['value'] == output_value
        return result
