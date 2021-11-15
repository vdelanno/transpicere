import unittest
import pyodbc
import string
import shortuuid
from transpicere.generator.db import DbConfig, DbGenerator, Node, Field, Query

ALPHABET = string.ascii_lowercase + string.digits
SU = shortuuid.ShortUUID(alphabet=ALPHABET)


class DbTestCase(unittest.TestCase):
    def setUp(self):
        self.connection_string = "Driver={PostgreSQL ANSI};Uid=user;Pwd=password;Server=localhost;Port=5432;Database=postgres_transpicere;Pooling=true;Min Pool Size=0;Max Pool Size=100;Connection Lifetime=0;"

        self.table_name = f"test_{SU.random(length=8)}"
        print(f"using table {self.table_name}")
        with pyodbc.connect(self.connection_string) as cnxn:
            cursor = cnxn.cursor()
            cursor.execute(f'''
                CREATE TABLE {self.table_name} (
                        bool_value BOOLEAN PRIMARY KEY,
                        int_value INTEGER,
                        bigint_value BIGINT,
                        text_value TEXT,
                        varchar_value VARCHAR[5],
                        float_value FLOAT,
                        datetime_value TIMESTAMP,
                        date_value DATE,
                        time_value TIME,
                        decimal_value DECIMAL,
                        uuid_value UUID
                );
                ''')
            cursor.execute(f'''
                CREATE INDEX index_name
                ON {self.table_name} (bigint_value, time_value);
                ''')

            cursor.commit()

    def tearDown(self):
        with pyodbc.connect(self.connection_string) as cnxn:
            cursor = cnxn.cursor()
            cursor.execute(f'''
            DROP TABLE {self.table_name}
            ''')
            cursor.commit()

    def test_db(self):
        cfg = DbConfig(connection_string=self.connection_string,
                       table=self.table_name)
        gen = DbGenerator()
        node = gen.get_node(config=cfg)
        print(node)
        assert node == Node(
            name=f"postgres_transpicere_{self.table_name}",
            fields={
                'bool_value': Field(data_type='Boolean', is_nullable=True, is_list=False),
                'int_value': Field(data_type='Int', is_nullable=True, is_list=False),
                'bigint_value': Field(data_type='Long', is_nullable=True, is_list=False),
                'text_value': Field(data_type='String', is_nullable=True, is_list=False),
                'varchar_value': Field(data_type='String', is_nullable=True, is_list=False),
                'float_value': Field(data_type='Float', is_nullable=True, is_list=False),
                'datetime_value': Field(data_type='Datetime', is_nullable=True, is_list=False),
                'date_value': Field(data_type='Date', is_nullable=True, is_list=False),
                'time_value': Field(data_type='Time', is_nullable=True, is_list=False),
                'decimal_value': Field(data_type='Decimal', is_nullable=True, is_list=False),
                'uuid_value': Field(data_type='UUID', is_nullable=True, is_list=False)
            },
            queries={
                f'{node.name}_bool_value': Query(
                    unique=True,
                    return_type=node.name,
                    params={
                        'bool_value': Field(data_type='Boolean', is_nullable=False, is_list=False)
                    }
                ),
                f'{node.name}_index_name': Query(
                    unique=False,
                    return_type=node.name, params={
                        'bigint_value': Field(data_type='Long', is_nullable=False, is_list=False),
                        'time_value': Field(data_type='Time', is_nullable=False, is_list=False)
                    }
                )
            }
        )
