import numpy as np
import pandas as pd
from string import punctuation
from postgresql_handler import PostgreSQLHandler

import re, nltk, spacy, string

class DataPreProcessor(object):
    def __init__(self):
        super().__init__()

    def clean_text(self, text:str, remove_punc=True)->str:
        '''
        Lowercase
        Remove punctuation
        Remove word containing numbers
        '''
        text = text.lower()
        text = re.sub(r'\w*\d\w*', '', text)
        if remove_punc == True:
            text = re.sub(r'[%s]' % re.escape(punctuation), '', text)

        return text

    def lemmatize(self, nlp, text):
        pass

if __name__ == '__main__':
    processor = DataPreProcessor()
    psql = PostgreSQLHandler()
    nlp = spacy.load("en_core_web_sm")
    print(type(nlp))
    sql = 'SELECT therapist_id, writing_sample FROM therapists'
    df = psql.sql_to_pandas(sql)
    
    df_clean = pd.DataFrame(df['writing_sample'].apply(lambda x: processor.clean_text(x)))

    #print(df_clean.head())


    

    psql.close_conn()