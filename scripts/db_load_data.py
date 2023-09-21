import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="bg",
  password="bg_data",
  database="bg_database"
)

cursor = mydb.cursor()

def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        cursor.execute(command)

executeScriptsFromFile('./db/migration/sql/V01__schema_test.sql')