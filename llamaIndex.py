import os
from sqlalchemy import create_engine, text
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index import SQLDatabase
from llama_index.llms import OpenAI
import mysql.connector as mysql

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, force=True)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from IPython.display import Markdown, display

db_user = "bg"
db_password = "bg_data"
db_host = "127.0.0.1"
db_name = "bg_database"

# Construct the connection string
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

# Create an engine instance
engine = create_engine(connection_string)

# Test the connection using raw SQL
with engine.connect() as connection:
    result = connection.execute(text("select * from report limit 2"))
    for row in result:
        print(row)

sql_database = SQLDatabase(engine, sample_rows_in_table_info=2)

#print(sql_database.table_info)
print(sql_database._usable_tables)
  
OPEN_API_KEY = os.environ["OPENAI_API_KEY"]

import tiktoken
from llama_index.callbacks import CallbackManager, TokenCountingHandler
token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
)

callback_manager = CallbackManager([token_counter])
     
from llama_index import ServiceContext, LLMPredictor, OpenAIEmbedding, PromptHelper
llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(
  llm=llm,callback_manager=callback_manager
)

from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    service_context=service_context
)
     
query_str = "how many entity are there?"
response = query_engine.query(query_str)
print(response.response)
print(response.metadata['result'])
print(token_counter.total_llm_token_count)

"""
print()
print(response.metadata['sql_query'])
print()
print(response.metadata['result'])
print()
print(token_counter.total_llm_token_count)"""

"""
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
"""
