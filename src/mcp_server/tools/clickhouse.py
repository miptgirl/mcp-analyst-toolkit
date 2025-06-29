import requests
import io
import pandas as pd
CH_HOST = 'http://localhost:8123' # default address 

def execute_query(query, host = CH_HOST, connection_timeout = 1500):
  r = requests.post(host, params = {'query': query}, 
    timeout = connection_timeout)
  if r.status_code == 200:
      return r.text
  else: 
      return 'Database returned the following error:\n' + r.text
      # giving feedback to LLM instead of raising exception

def get_databases(host = CH_HOST, connection_timeout = 1500):
    return execute_query('show databases', host, connection_timeout)

def get_table_schema(table_name, host = CH_HOST, connection_timeout = 1500):
    query = f"DESCRIBE TABLE {table_name}"
    return execute_query(query, host, connection_timeout)