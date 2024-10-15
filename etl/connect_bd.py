###------------------------------------------------------------------------------------------------
## Description: Connect to the database, execute SQL queries, and insert new data into database tables.
###------------------------------------------------------------------------------------------------


##------------------------
## REQUIRED PACKAGES
##------------------------

## Conexão com o banco de dados SQLServer
from sqlalchemy import create_engine
import pandas as pd
import os
import ast




##-----------------
## FUNCTIONS
##-----------------

## INSERT DATA
def insert(table_name, df):

    ##----------------------
    ## ACCESS CREDENTIALS - BD
    ##----------------------

    # Gets the directory where the script is located
    main_dir = os.path.dirname(os.path.abspath(__file__))

    # Create relative path from script directory
    relative_path = os.path.join(main_dir, 'credentials_bd.txt')
    # Open the txt file in reading mode
    with open(relative_path, 'r') as file:
        credentials_bd = file.read()
    ## Moving to dictionary
    credentials_bd = ast.literal_eval(credentials_bd)

    ## Connection to the SQLServer database
    server_name = credentials_bd['server_name']
    database_name = credentials_bd['database_name']
    username = credentials_bd['username']
    password = credentials_bd['password']

    print('Here are your credentials')
    print('server_name: ', server_name)
    print('database_name: ', database_name)
    print('username: ', username)
    print('password: ', password)

    connection_string = f"mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"
    # Create an SQLAlchemy engine
    engine = create_engine(connection_string)
    # Specify the table name in your database where you want to store the data
    table_name = table_name
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print('Data saved in table ', table_name)

    ## Closing the connection
    engine.dispose()


## SELECT QUERY
def query_bd(query):

    ##----------------------
    ## ACCESS CREDENTIALS - BD
    ##----------------------

    # Gets the directory where the script is located
    main_dir = os.path.dirname(os.path.abspath(__file__))

    # Create relative path from script directory
    relative_path = os.path.join(main_dir, 'credentials_bd.txt')
    # Open the txt file in reading mode
    with open(relative_path, 'r') as file:
        credentials_bd = file.read()
    ## Moving to dictionary
    credentials_bd = ast.literal_eval(credentials_bd)


    # Replace these placeholders with your SQL Server credentials and database information
    server_name = credentials_bd['server_name']
    database_name = credentials_bd['database_name']
    username = credentials_bd['username']
    password = credentials_bd['password']

    print('Here are your credentials')
    print('server_name: ', server_name)
    print('database_name: ', database_name)
    print('username: ', username)
    print('password: ', password)


    # Create a connection string
    connection_string = f"mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"


    # Create an SQLAlchemy engine
    engine = create_engine(connection_string)

    # Running the query
    df = pd.read_sql(query, engine)

    ## Closing the Connection
    engine.dispose()

    return(df)
