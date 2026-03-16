import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate

load_dotenv()

db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]

# Create an SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")

# Create an instance of SQLDatabase
db = SQLDatabase(engine)

PROMPT_SUFFIX = """

Only use the following tables:
{table_info}

Use the following database schema for reference:
'''create table report
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

Question: {input}"""

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. 

Use the following database schema for reference:
'''create table report
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

Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

"""

llm = LlamaCpp(
    model_path="/Users/quay17/Desktop/GitLocal/NLP/llama2/llama-2-7b.Q4_K_M.gguf", 
    verbose=True, 
    n_ctx=2048)

PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect", "top_k"],
    template=_DEFAULT_TEMPLATE + PROMPT_SUFFIX,
)

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_sql=True, 
                                     prompt=PROMPT)

input_question = "What is the Recipient Paid for Administrative and Support and Waste Management and Remediation Services industry in San Miguel Co for June 2022?"

table_info = lambda x: db.get_table_info(
            table_names=x.get("table_names_to_use"))

formatted_prompt = PROMPT.format(
    input=input_question, 
    table_info=table_info,
    dialect="mysql",  # Replace with your database's dialect if different
    top_k=2           # Adjust as needed
)

import langchain
langchain.debug = True

response = db_chain.run(formatted_prompt)
print(response)

