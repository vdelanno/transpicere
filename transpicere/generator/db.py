# mypy: allow-untyped-defs
import pyodbc
import logging
from typing import Dict, List, TypeVar, Any
from decimal import Decimal
from datetime import date, time, datetime
from uuid import UUID
from dataclasses import dataclass, field
from transpicere.graphql import *

LOGGER = logging.Logger(__name__)
TYPE_MAPPING = {
    'bool': GraphQLBoolean.name,
    'int2': GraphQLInt.name,
    'int4': GraphQLInt.name,
    'int8': GraphQLLong.name,
    'text': GraphQLString.name,
    '_varchar': GraphQLString.name,
    'float4': GraphQLFloat.name,
    'float8': GraphQLFloat.name,
    'numeric': GraphQLDecimal.name,
    'date': GraphQLDate.name,
    'time': GraphQLTime.name,
    'timestamp': GraphQLDatetime.name,
    'uuid': GraphQLUuid.name
}


@dataclass
class Field:
    data_type: str
    is_nullable: bool = field(default=True)
    is_list: bool = field(default=False)


@dataclass
class Query:
    unique: bool
    return_type: str
    params: Dict[str, Field] = field(default_factory=dict)


@dataclass
class Node:
    name: str
    fields: Dict[str, Field]
    queries: Dict[str, Query]


@ dataclass
class DbConfig:
    connection_string: str
    table: str


class DbGenerator:

    def get_node(self, config: DbConfig) -> Node:
        with pyodbc.connect(config.connection_string) as cnxn:
            cursor = cnxn.cursor()
            node_name = self._get_node_name(cursor, config)
            fields = self._get_fields(cursor, config)
            queries = self._get_queries(cursor, config, node_name, fields)

            return Node(
                name=node_name,
                fields=fields,
                queries=queries
            )

    def _get_node_name(self, cursor: pyodbc.Cursor, config: DbConfig) -> str:
        for table in cursor.tables():
            if table.table_name == config.table:
                return f"{table.table_cat}_{config.table}"
        raise ValueError(f"table {table} not found")

    def _get_fields(self, cursor: pyodbc.Cursor, config: DbConfig) -> Dict[str, Field]:
        rows = cursor.columns(table=config.table)
        fields = {
            row.column_name: Field(TYPE_MAPPING[row.type_name]) for row in rows
        }
        if len(fields) == 0:
            raise ValueError(f"table {config.table} has no column")
        return fields

    def _get_queries(self, cursor: pyodbc.Cursor, config: DbConfig, node_name: str, fields: Dict[str, Field]) -> Dict[str, Query]:
        indices = cursor.statistics(table=config.table)
        queries: dict[str, Query] = dict()
        for row in indices:
            query = queries.setdefault(
                row.index_name, Query(return_type=node_name, unique=not row.non_unique))
            query.params[row.column_name] = Field(
                fields[row.column_name].data_type, is_nullable=False)

        def query_name(index_name: str, query: Query) -> str:
            index = index_name
            if len(query.params) == 1:
                index = next(iter(query.params))
            return f"{node_name}_{index}"
        return {query_name(k, v): v for k, v in queries.items()}
