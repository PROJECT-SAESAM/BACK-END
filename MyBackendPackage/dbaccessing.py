from common import config, secret
import numpy as np
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


driver = secret.dbconfig.drivername.value
host = secret.dbconfig.host.value
port = secret.dbconfig.port.value
user = secret.dbconfig.user.value
password = secret.dbconfig.password.value
charset = secret.dbconfig.charset.value


# def engine(schema) :
#     return create_engine(f'mysql+pymysql://{user}:{password}@{host}/{schema}', encoding = charset)


# def conn(schema) :
#     return create_engine(f'mysql+pymysql://{user}:{password}@{host}/{schema}', encoding = charset).connect()



def engine(schema) :
    url = URL.create(
        drivername = driver,
        host = host,
        password = password, 
        port = port,
        username = user,
        database = f"{schema}",
        query = {'charset' : charset}
    )
    return create_engine(url)


def func_dbdownload(table_name, schema) :
    df = pd.read_sql(
        f"SELECT * FROM {table_name}", 
        con = engine(schema), 
        index_col = "index"
        )
    return df


def func_dbupload(df, table_name, schema) :
    df.to_sql(
    name = table_name, 
    con = engine(schema), 
    if_exists = 'replace', 
    index = True, 
    index_label = None, 
    chunksize = None, 
    dtype = None
    )
