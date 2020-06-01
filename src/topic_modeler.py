import psycopg2
import numpy as np
import pandas as pd
from string import punctuation
from visualizer import Visualizer
from data_pre_processor import DataPreProcessor
from postgresql_handler import PostgreSQLHandler

import re, nltk, spacy, string

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pprint import pprint

import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px

import argparse
import pickle

class TopicModeler(object):
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    

    


if __name__ == '__main__':
    # instantiate nlp processor
    tm = TopicModeler(log_file_path='logs/lda_results_log.txt')
    
    # define colors for visualizations
    palette = ['#13bdb4','#80d090','#dad977','#e49046','#d43d51']

    parser = argparse.ArgumentParser()
   
    parser.add_argument('-fd', '--fromdisk', action='store_true', 
        help="load data from local file")

    args = parser.parse_args()

    processor = DataPreProcessor()
    psql = PostgreSQLHandler()
    vis = Visualizer(psql.get_conn())
    vis.set_show_figs(True)
    vis.set_save_figs(False)

    df_processed = None
    processed_text_filename = 'data/df_processed_testing.pkl'
    min_doc_length = 200

    if args.fromdisk:
        df_processed = pickle.load( open( processed_text_filename, "rb" ) )
    else:
        sql = 'SELECT * FROM therapists'
        df = psql.sql_to_pandas(sql)
        top_n_percent_words = processor.get_top_n_percent_words(df['writing_sample'],.1)
        custom_stop_words = []
        additional_stops = top_n_percent_words + custom_stop_words
        df_processed = processor.processing_pipeline(df=df,text_col='writing_sample', min_doc_length= min_doc_length,
            additional_stop_words=additional_stops)
        print(df.head())
        pickle.dump(df_processed, open( processed_text_filename, "wb" ) )

    print(df_processed.head())

    
    

    # vis.word_distribution(df_processed)
    # vis.word_cloud(df_processed, 'writing_sample_processed')
    vis.ngram_bar_chart(df_processed['writing_sample_processed'],(1,1), 100)
    # vis.ngram_bar_chart(df_processed['writing_sample_processed'],(4,4), 20)

    tf_vectorizer = CountVectorizer(analyzer='word',       
                            min_df=3,                       
                            stop_words=processor.get_stop_words(),                      
                            token_pattern='[a-zA-Z0-9]{3,}',  
                            max_features=5000,          
                            )

    tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())

    vectorizer = tfidf_vectorizer

    data_vectorized = vectorizer.fit_transform(df_processed['writing_sample_processed'])

    lda_model = LatentDirichletAllocation(n_components=5, # Number of topics
                                        learning_method='online',
                                        random_state=0,       
                                        n_jobs = -1  # Use all available CPUs
                                        )
    lda_model.fit(data_vectorized)

    vis = pyLDAvis.sklearn.prepare(lda_model, data_vectorized, vectorizer)

    pyLDAvis.save_html(vis, 'vis/ldavis_tfidf')
