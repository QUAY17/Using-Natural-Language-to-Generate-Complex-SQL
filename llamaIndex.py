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

db_schema = '''create table report
(
    id                      INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    excel_file_name         varchar(128) NOT NULL,
    excel_tab_name          varchar(128) NOT NULL,
    revenue_group           varchar(128),
    business_activity_month DATE,
    reporting_month         DATE,
    distribution_month      DATE,
    report_run              DATETIME,
    start                   DATE,
    end                     DATE
);

create table industry_entity
(
    id        INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name      varchar(128) NOT NULL,
    entity_id INT NOT NULL,
    foreign key (entity_id) references entity (id),
    UNIQUE(name, entity_id)
);

create table entity
(
    id   INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(128) NOT NULL,
    code varchar(32) NOT NULL,
    UNIQUE(name)
);

create table industry_entity_tax
(
    id                       BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    report_id                INT NOT NULL,
    industry_entity_id       INT NOT NULL,
    name                     varchar(128) NOT NULL,
    returns                  DOUBLE,
    total_receipts           DOUBLE,
    taxable_receipts         DOUBLE,
    matched_taxable_receipts DOUBLE,
    total_tax_due            DOUBLE,
    total_tax_paid           DOUBLE,
    recipient_paid           DOUBLE,
    recipient_due            DOUBLE,
    adjustment               DOUBLE,
    foreign key (report_id) references report (id),
    foreign key (industry_entity_id) references industry_entity (id)
);'''

sql_database = SQLDatabase(engine, sample_rows_in_table_info=2)

#print(sql_database.table_info)
print(sql_database._usable_tables)
print(list(sql_database._all_tables))
print(sql_database.get_single_table_info("entity"))


OPEN_API_KEY = os.environ["OPENAI_API_KEY"]
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
