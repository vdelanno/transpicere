from typing import List
from transpicere.generator.configuration import Config
from transpicere.generator.node import Node
from typing import Dict, Callable, Union
from graphql.type import GraphQLType, GraphQLSchema
from transpicere.graphql import GraphQLBool, GraphQLUuid, GraphQLDecimal, GraphQLDatetime, GraphQLDate, GraphQLTime, GraphQLLong
from dataclasses import dataclass, field

BASE_TYPES = [GraphQLBool, GraphQLUuid, GraphQLDecimal,
              GraphQLDatetime, GraphQLDate, GraphQLTime, GraphQLLong]


@dataclass
class SchemaFactoryCache:
    types: Dict[str, Union[Callable[[], GraphQLType],
                           GraphQLType]] = field(default_factory=dict)


class NodeFactory:
    def __init__(self) -> None:
        pass


class SchemaFactory:
    def __init__(self, node_factories: List[NodeFactory]):
        self._node_factories = node_factories

    def generate_schema(self, configs: List[Config]) -> None:
        cache = SchemaFactoryCache()
        cache.types = {t.name: t for t in BASE_TYPES}
        for config in configs:
            self.handle_config(config)
        return None

    def handle_config(self, config: Config) -> None:

        pass

    def node_to_graphql(self, node: Node) -> None:
        pass
