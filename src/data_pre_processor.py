import numpy as np
import pandas as pd
from string import punctuation
from postgresql_handler import PostgreSQLHandler
from spacy.lang.en.stop_words import STOP_WORDS as spacy_stops

import re, nltk, spacy, string

import argparse

class DataPreProcessor(object):
    def __init__(self):
        self.nlp = spacy.load("en")
        self.all_stop_words = spacy_stops
        self.custom_stop_words = None

    def add_stop_words(self, custom_stops:list)->None:
        self.all_stop_words = list(set(self.all_stop_words + custom_stops))

    def remove_top_n_percent_words(self, tf_matrix:np.matrix, n_percent:int)->np.matrix:
        pass

    def drop_short_docs(self, df:pd.DataFrame, text_col:str, min_length:int)->pd.DataFrame:
        '''
        drop rows where text is shorter than specified length
        '''
        df_truncated = df[df[text_col].str.len() >= min_length]

        return df_truncated

    def clean_text(self, text:str, remove_punc=True)->str:
        # Lowercase
        text = text.lower()
        # Remove word containing numbers
        text = re.sub(r'\w*\d\w*', '', text)

        if remove_punc == True:
            text = re.sub(r'[%s]' % re.escape(punctuation), '', text)

        # remove newline and return characters
        text = re.sub(r'[%s]' % re.escape('\n'), '', text)
        text = re.sub(r'[%s]' % re.escape('\r'), '', text)

        return text

    # lemmatize with spaCy
    def lemmatize(self, nlp, text:str)->str:
        lemmed = []
        doc = nlp(text)

        for word in doc:
            lemmed.append(word.lemma_)
        
        return ' '.join(lemmed)

    def processing_pipeline(self, df:pd.DataFrame, min_doc_length:int)->pd.DataFrame:
        df_clean = self.drop_short_docs(df ,'writing_sample', min_doc_length)
        # initial text cleaning
        df_clean['writing_sample_clean'] = pd.DataFrame(df_clean['writing_sample'].apply(lambda x: self.clean_text(x)))
        # lemmatize with spaCy
        df_clean['writing_sample_lemmatize'] = df_clean.apply(lambda x: self.lemmatize(self.nlp, x['writing_sample']), axis=1)
        # remove spaCy -PRON-
        df_clean['writing_sample_processed'] = df_clean['writing_sample_lemmatize'].str.replace('-PRON-', '')

        

        return df_clean

if __name__ == '__main__':
    from visualizer import Visualizer
    import pickle

    parser = argparse.ArgumentParser()
   
    parser.add_argument('-fd', '--fromdisk', action='store_true', 
        help="load data from local file")

    args = parser.parse_args()

    


    processor = DataPreProcessor()
    psql = PostgreSQLHandler()
    vis = Visualizer(psql.get_conn())
    vis.set_show_figs(True)
    vis.set_save_figs(False)

    load_from_disk = False
    df_processed = None
    #if load_from_disk:
    if args.fromdisk:
        df_processed = pickle.load( open( 'data/df_processed_testing.pkl', "rb" ) )
    else:
        sql = 'SELECT * FROM therapists LIMIT 1000'
        df = psql.sql_to_pandas(sql)
        
        df_processed = processor.processing_pipeline(df)
        print(df.head())
        pickle.dump(df_processed, open( 'data/df_processed_testing.pkl', "wb" ) )

    print(df_processed.head())

    #vis.word_distribution(df_processed)
    #vis.word_cloud(df_processed, 'writing_sample_processed')
    #vis.ngram_bar_chart(df_processed['writing_sample_processed'],(1,1), 40)
    #vis.ngram_bar_chart(df_processed['writing_sample_processed'],(4,4), 20)

    psql.close_conn()


    