import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index import SQLDatabase
from llama_index.llms import OpenAI

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, force=True)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()

db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]

# Construct the connection string
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

# Create an engine instance
engine = create_engine(connection_string)

sql_database = SQLDatabase(engine, sample_rows_in_table_info=2)

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

