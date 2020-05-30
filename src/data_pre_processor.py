import numpy as np
import pandas as pd
from string import punctuation
from postgresql_handler import PostgreSQLHandler
from spacy.lang.en.stop_words import STOP_WORDS

import re, nltk, spacy, string

class DataPreProcessor(object):
    def __init__(self):
        self.nlp = spacy.load("en")

    def clean_text(self, text:str, remove_punc=True)->str:
        # Lowercase
        text = text.lower()
        # Remove word containing numbers
        text = re.sub(r'\w*\d\w*', '', text)

        if remove_punc == True:
            text = re.sub(r'[%s]' % re.escape(punctuation), '', text)

        # remove newlines
        text = re.sub(r'[%s]' % re.escape('\n'), '', text)
        text = re.sub(r'[%s]' % re.escape('\r'), '', text)

        return text

    def lemmatize(self, nlp, text:str)->str:
        lemmed = []
        doc = nlp(text)

        for word in doc:
            lemmed.append(word.lemma_)
        
        return ' '.join(lemmed)

    def processing_pipeline(self, df:pd.DataFrame)->pd.DataFrame:
        # initial text cleaning
        df_clean = pd.DataFrame(df['writing_sample'].apply(lambda x: self.clean_text(x)))
        # lemmatize with spaCy
        df_clean['writing_sample_lemmatize'] = df_clean.apply(lambda x: self.lemmatize(self.nlp, x['writing_sample']), axis=1)
        # remove spaCy -PRON-
        df_clean['writing_sample_processed'] = df_clean['writing_sample_lemmatize'].str.replace('-PRON-', '')

        return df_clean

if __name__ == '__main__':
    from visualizer import Visualizer
    import pickle

    processor = DataPreProcessor()
    psql = PostgreSQLHandler()
    vis = Visualizer(psql.get_conn())
    vis.set_show_figs(True)
    vis.set_save_figs(False)

    # sql = 'SELECT * FROM therapists LIMIT 100'
    # df = psql.sql_to_pandas(sql)
    
    # df_processed = processor.processing_pipeline(df)
    # print(df.head())
    # pickle.dump(df_processed, open( 'data/df_processed_testing.pkl', "wb" ) )
    df_processed = pickle.load( open( 'data/df_processed_testing.pkl', "rb" ) )

    
    print(df_processed.head())

    #vis.word_distribution(df_processed)
    #vis.word_cloud(df_processed, 'writing_sample_processed')
    vis.ngram_bar_chart(df_processed['writing_sample_processed'],(1,1), 40)
    vis.ngram_bar_chart(df_processed['writing_sample_processed'],(4,4), 20)
    psql.close_conn()


    