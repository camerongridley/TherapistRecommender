import psycopg2
import pandas as pd

class PostgreSQLHandler(object):

    def __init__(self):
        self.conn = self.open_conn()

    def open_conn(self):
        return psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')

    def get_conn(self):
        return self.conn

    def close_conn(self):
        self.conn = None

    def sql_to_pandas(self, sql:str)->pd.DataFrame:
        df = pd.read_sql_query(sql, self.conn)

        return df