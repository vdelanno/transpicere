from typing import List, Any, Dict
import unittest
import pytest
from parameterized import parameterized
import sqlite3
import pyodbc
import string
import shortuuid
import platform
from transpicere.generator.db import DbConfig, DbGenerator, Node, Field, Query

# ALPHABET = string.ascii_lowercase + string.digits
ALPHABET = string.ascii_lowercase
SU = shortuuid.ShortUUID(alphabet=ALPHABET)

FIELD_TYPES = {
    'boolean_value':    'Boolean',
    'integer_value':    'Int',
    'bigint_value':     'Long',
    'text_value':       'String',
    'varchar_value':    'String',
    'float_value':      'Float',
    'timestamp_value':  'Datetime',
    'date_value':       'Date',
    'time_value':       'Time',
    'decimal_value':    'Decimal',
    'uuid_value':       'UUID',
}


def make_pairs(l: List[Any]):
    return [l[i:i+2] for i in range(0, len(l)-1)]


class TestDbConfig(unittest.TestCase):
    def setUp(self):
        # self.connection_string = "DRIVER={SQLite3 ODBC Driver};SERVER=localhost;DATABASE=transpicere;Trusted_connection=yes"
        self.db_name = "postgres_transpicere"
        self.table_name = f"test_{SU.random(length=8)}"
        print(f"using table {self.table_name}")

        self.connection_string = "Driver={PostgreSQL UNICODE};Uid=user;Pwd=password;Server=postgres;Port=5432;Database=postgres_transpicere;Pooling=true;Min Pool Size=0;Max Pool Size=100;Connection Lifetime=0;"

        with pyodbc.connect(self.connection_string) as cnxn:
            cursor = cnxn.cursor()
            cursor.execute(f'''
                CREATE TABLE {self.table_name} (
                    boolean_value BOOLEAN,
                    integer_value INTEGER,
                    bigint_value BIGINT,
                    text_value TEXT,
                    varchar_value VARCHAR[5],
                    float_value FLOAT,
                    timestamp_value TIMESTAMP,
                    date_value DATE,
                    time_value TIME,
                    decimal_value DECIMAL,
                    uuid_value UUID
                );
                ''')
            cursor.commit()

    def tearDown(self):
        with pyodbc.connect(self.connection_string) as cnxn:
            cursor = cnxn.cursor()
            cursor.execute(f'DROP TABLE {self.table_name}')
            cursor.commit()

    def create_index(self, name, unique, indices: List[str]):
        with pyodbc.connect(self.connection_string) as cnxn:
            cursor = cnxn.cursor()
            cursor.execute(f'''
                CREATE {'UNIQUE' if unique else ''} INDEX {name}
                ON {self.table_name} ({', '.join(indices)});
                ''')

            cursor.commit()

    def insert_sample_data(self, rows: List[Dict[str, Any]]):
        with pyodbc.connect(self.connection_string, autocommit=True) as cnxn:
            cursor = cnxn.cursor()
            cursor.executemany(f"insert into {self.table_name}")

    def test_column(self):
        cfg = DbConfig(connection_string=self.connection_string,
                       table=self.table_name)
        gen = DbGenerator()
        node = gen.get_node(config=cfg)
        print(node)
        assert node.name == f"postgres_transpicere_{self.table_name}"
        assert node.fields == {
            field_name: Field(data_type=field_type,
                              is_nullable=True, is_list=False)
            for field_name, field_type in FIELD_TYPES.items()
        }

    @ parameterized.expand([
        (field_name1, field_type1, field_name2, field_type2, unique)
        for (field_name1, field_type1), (field_name2, field_type2) in make_pairs(list(FIELD_TYPES.items()))
        for unique in [True, False]
    ])
    def test_composed_index(self, field_name1, field_type1, field_name2, field_type2, unique: bool):
        index_name = f'{field_name1}_{field_name2}'
        self.create_index(index_name, unique, [field_name1, field_name2])

        cfg = DbConfig(connection_string=self.connection_string,
                       table=self.table_name)
        gen = DbGenerator()
        node = gen.get_node(config=cfg)
        print(node.queries)
        query_name = f"{node.name}_{index_name}"
        assert len(node.queries) == 1
        assert query_name in node.queries
        query = node.queries[list(node.queries.keys())[0]]
        assert not query.is_list == unique
        assert query.return_type == node.name
        assert query.params == {
            field_name1: Field(data_type=field_type1,
                               is_nullable=False,
                               is_list=False),
            field_name2: Field(data_type=field_type2,
                               is_nullable=False,
                               is_list=False)
        }

    @ parameterized.expand([
        (field_name, field_type, unique)
        for field_name, field_type in FIELD_TYPES.items()
        for unique in [True, False]
    ])
    def test_simple_index(self, field_name, field_type, unique):
        self.create_index('unused_value', unique, [field_name])

        cfg = DbConfig(connection_string=self.connection_string,
                       table=self.table_name)
        gen = DbGenerator()
        node = gen.get_node(config=cfg)
        print(node.queries)
        query_name = f'{node.name}_{field_name}'
        assert query_name in node.queries
        assert len(node.queries) == 1
        query = node.queries[query_name]
        assert not query.is_list == unique
        assert query.return_type == node.name
        assert query.params == {
            field_name: Field(data_type=field_type,
                              is_nullable=False,
                              is_list=False)
        }


class TestDbResolver(unittest.TestCase):
    def setUp(self):
        self.db_name = f"test_{SU.random(length=8)}.db"
        self.table_name = f"test_{SU.random(length=8)}"
        driver = "SQLite3"
        if platform.system() == "Windows":
            driver = "{SQLite3 ODBC Driver}"

        self.connection_string = f"DRIVER={driver};DATABASE=file:{self.db_name};"
        print(f"using db {self.db_name}")
        print(f"using connection {self.connection_string}")
        print(f"using table {self.table_name}")
        with sqlite3.connect(self.db_name) as con:
            con.commit()

    def test_query(self):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            cur.execute(
                f"CREATE TABLE {self.table_name} (data TEXT NOT NULL PRIMARY KEY)")
            cur.executemany(
                f"INSERT INTO {self.table_name} VALUES (?)", [
                    ("value1",),
                    ("value2",),
                    ("value3",)
                ])
            con.commit()
            # cur.execute("CREATE UNIQUE INDEX col1 ON test_table (col1)")
            print("db initialized")
        cfg = DbConfig(connection_string=self.connection_string,
                       table=self.table_name)
        gen = DbGenerator()
        node = gen.get_node(config=cfg)
        assert len(node.queries) == 1
        query = node.queries[next(iter(node.queries.keys()))]
        print(query)
        result = query.resolver(data="value2")
        assert list(result) == [{
            'data': 'value2'
        }]
