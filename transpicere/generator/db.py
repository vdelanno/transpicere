# mypy: allow-untyped-defs
from graphql.type.definition import GraphQLField, GraphQLScalarType
import pyodbc
import logging
from typing import Dict, List, TypeVar, Any, Callable, Iterator, Generator
from decimal import Decimal
from datetime import date, time, datetime
from uuid import UUID
from dataclasses import dataclass, field
from transpicere.graphql import *
from transpicere.generator.node import Node, Field, Query
from transpicere.generator.configuration import ConfigImpl
from transpicere.generator.base_types import BaseType

LOGGER = logging.Logger(__name__)


def get_field_type(db_type_str: str) -> str:
    db_type = db_type_str.lower()
    if db_type.startswith('bool'):
        return GraphQLBool.name
    if db_type.startswith('int') and db_type not in ('int8', 'int16'):
        return GraphQLLong.name
    if db_type.startswith('int') or db_type.startswith('bigint'):
        return GraphQLLong.name
    if db_type.startswith('float'):
        return GraphQLDouble.name
    if db_type == 'text' or db_type.startswith('_varchar') or db_type.startswith('varchar'):
        return GraphQLString.name
    if db_type == 'numeric' or db_type == 'decimal':
        return GraphQLDecimal.name
    if db_type == 'date':
        return GraphQLDate.name
    if db_type == 'time':
        return GraphQLTime.name
    if db_type == 'timestamp' or db_type == 'datetime':
        return GraphQLDatetime.name
    if db_type == 'uuid':
        return GraphQLUuid.name
    raise ValueError(
        f"db type {db_type_str} not recognize. Please provide handler")


DATA_CONVERTERS = {
    t.name: t.parse_value for t in [GraphQLBool, GraphQLLong, GraphQLDouble, GraphQLString, GraphQLDecimal, GraphQLDate, GraphQLTime, GraphQLDatetime, GraphQLUuid]
}


@ dataclass
class DbConfig(ConfigImpl):
    connection_string: str
    table: str


class DbResolver:
    def __init__(self, config: DbConfig, is_list: bool, fields: Dict[str, Field]):
        self._config = config
        self._is_list = is_list
        self._converters = {
            name: DATA_CONVERTERS[field.data_type] for name, field in fields.items()}

    def __call__(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        (placeholders, bindings) = zip(*kwargs.items())
        where_clause = ' AND '.join([f"{p}=?" for p in placeholders])
        statement = f"select * from {self._config.table} where {where_clause}"
        with pyodbc.connect(self._config.connection_string) as cnxn:
            cursor = cnxn.cursor()
            rows = cursor.execute(statement, bindings)
            column_names = [desc[0] for desc in cursor.description]
            return [self._row_to_dict(row, column_names) for row in rows]
            # row = next(rows, None)
            # if self._is_list:
            #     print(row)
            #     while row:
            #         yield self._row_to_dict(row, column_names)
            #         row = next(row, None)
            # else:

    def _row_to_dict(self, row: List[Any], column_names: List[str]) -> Dict[str, Any]:
        data = dict(zip(column_names, row))
        return {name: self._converters[name](value) for name, value in data.items()}


class DbGenerator():
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
            row.column_name: Field(get_field_type(row.type_name)) for row in rows
        }
        if len(fields) == 0:
            raise ValueError(f"table {config.table} has no column")
        return fields

    def _get_queries(self, cursor: pyodbc.Cursor, config: DbConfig, node_name: str, fields: Dict[str, Field]) -> Dict[str, Query]:
        indices = cursor.statistics(table=config.table)
        queries: dict[str, Query] = dict()
        for row in indices:
            query = queries.setdefault(
                row.index_name, Query(
                    return_type=node_name,
                    is_list=row.non_unique,
                    resolver=DbResolver(config, row.non_unique, fields)
                )
            )
            query.params[row.column_name] = Field(
                fields[row.column_name].data_type,
                is_nullable=False)

        def query_name(index_name: str, query: Query) -> str:
            index = index_name
            if len(query.params) == 1:
                index = next(iter(query.params))
            return f"{node_name}_{index}"

        return {query_name(k, v): v for k, v in queries.items()}
