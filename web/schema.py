from transpicere.graphql import *
import pyodbc
from graphql import GraphQLField, GraphQLSchema, GraphQLObjectType
from graphql import GraphQLString


def init_db():
    connection_string = "Driver={PostgreSQL ANSI};Uid=user;Pwd=password;Server=localhost;Port=5432;Database=postgres_transpicere;Pooling=true;Min Pool Size=0;Max Pool Size=100;Connection Lifetime=0;"
    table_name = f"sample"
    print(f"using table {table_name}")
    with pyodbc.connect(connection_string) as cnxn:
        cursor = cnxn.cursor()
        cursor.execute(f'''
                CREATE TABLE {table_name} (
                        bool_value BOOLEAN,
                        int_value INTEGER PRIMARY KEY,
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
                ON {table_name} (bigint_value);
                ''')

        insert_statement = f"""
        INSERT INTO {table_name}
        (bool_value, int_value, bigint_value, text_value, varchar_value, float_value, datetime_value, date_value, time_value, decimal_vlue, uuid_value)
        VALUES
        ()
        """
        cursor.commit()


def get_schema() -> GraphQLSchema:
    schema = GraphQLSchema(
        query=GraphQLObjectType(
            name='RootQueryType',
            fields={
                'hello': GraphQLField(
                    GraphQLString,
                    resolve=lambda obj, info: 'me!')
            }))

    return schema
