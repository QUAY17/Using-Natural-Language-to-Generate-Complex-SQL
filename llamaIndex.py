import os
from sqlalchemy import create_engine
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index import SQLDatabase
from llama_index.llms import OpenAI
import mysql.connector as mysql


OPEN_API_KEY = os.environ["OPENAI_API_KEY"]

try:
    with mysql.connect(
        host='localhost',
        user='bg',
        password='bg_data',
        database='bg_database'
    ) as conn:
        print("Successfully connected to the database")
except mysql.Error as err:
    print(f"Error: {err}")

db_uri = "mysql+mysqlconnector://bg:bg_data@localhost/bg_database"

llm = OpenAI(temperature=0.0, model_path="gpt-4-turbo")

db_engine = create_engine(db_uri)
sql_db = SQLDatabase(db_engine)

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_db,
)

query_str = "how many entities are there?"
response = query_engine.query(query_str)
print(response.response)
print()
print(response.metadata['sql_query'])