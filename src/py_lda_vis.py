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
from sklearn.decomposition import NMF
from pprint import pprint

import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px

import argparse
import pickle

from spacy.lang.en.stop_words import STOP_WORDS as spacy_stops

class TopicModeler(object):
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.stop_words = spacy_stops

    def show_topics(self, vectorizer, lda_model, n_words=20):
        keywords = np.array(vectorizer.get_feature_names())
        topic_keywords = []
        
        for topic_weights in lda_model.components_:
            top_keyword_locs = (-topic_weights).argsort()[:n_words]
            topic_keywords.append(keywords.take(top_keyword_locs))

        df_topic_keywords = pd.DataFrame(topic_keywords)
        df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
        df_topic_keywords.index = ['Topic '+str(i) for i in range(df_topic_keywords.shape[0])]
        df_topic_keywords

        return df_topic_keywords

    def label_theme(self, row, topics_theme):
            if row['dominant_topic'] == 0 :
                return topics_theme[0]
            if row['dominant_topic'] == 1 :
                return topics_theme[1]
            if row['dominant_topic'] == 2 :
                return topics_theme[2]
            if row['dominant_topic'] == 3:
                return topics_theme[3]
            if row['dominant_topic']  == 4:
                return topics_theme[4]

    def run_lda(self, df_processed, text_col, vectorizer, data_vectorized):
        lda_model = LatentDirichletAllocation(n_components=4, # Number of topics
                                        learning_method='online',
                                        random_state=0,       
                                        n_jobs = -1  # Use all available CPUs
                                        )
        lda_model.fit(data_vectorized)

        df_topic_keywords = self.show_topics(vectorizer=vectorizer, lda_model=lda_model, n_words=20)
        #print(df_topic_keywords)

        topics_theme = ['Topic Theme 0', 'Topic Theme 1', 'Topic Theme 2', 'Topic Theme 3']
        df_topic_keywords['topic_theme'] = topics_theme
        df_topic_keywords.set_index('topic_theme', inplace=True)
        
        print(df_topic_keywords.T)


        doc_topic_matrix = lda_model.transform(data_vectorized)
        # column names
        topicnames = df_topic_keywords.T.columns

        # index names
        docnames = ["Doc" + str(i) for i in range(len(df_processed))]

        # Make the pandas dataframe
        df_document_topic = pd.DataFrame(np.round(doc_topic_matrix, 2), columns=topicnames, index=docnames)

        # Get dominant topic for each document
        dominant_topic = np.argmax(df_document_topic.values, axis=1)
        df_document_topic['dominant_topic'] = dominant_topic

        df_document_topic.reset_index(inplace=True)
        df_sent_topic= pd.merge(df_processed, df_document_topic, left_index=True, right_index=True)
        df_sent_topic.drop('index', axis=1, inplace=True)

        df_topic_theme = df_sent_topic[[text_col, 'dominant_topic']]
                
        df_topic_theme['dominant_topic_theme'] = df_topic_theme.apply (lambda row: self.label_theme(row, topics_theme), axis=1)
        print(df_topic_theme.head(15))

        vis = pyLDAvis.sklearn.prepare(lda_model, data_vectorized, vectorizer)

        pyLDAvis.save_html(vis, 'vis/ldavis_tfidf')

if __name__ == '__main__':
    # instantiate nlp processor
    tm = TopicModeler(log_file_path='logs/lda_results_log.txt')
    original_text_col = 'writing_sample'
    process_text_col = 'text_processed'
    
    # define colors for visualizations
    palette = ['#13bdb4','#80d090','#dad977','#e49046','#d43d51']

    processor = DataPreProcessor(text_processed_colname=process_text_col)
    psql = PostgreSQLHandler()
    vis = Visualizer(psql.get_conn())
    vis.set_show_figs(True)
    vis.set_save_figs(False)

    df_processed = None
    processed_text_filename = 'data/df_processed_testing.pkl'
    min_doc_length = 200

    parser = argparse.ArgumentParser()
   
    parser.add_argument('-fd', '--fromdisk', action='store_true', 
        help="load data from local file")

    args = parser.parse_args()

    if args.fromdisk:
        df_processed = pickle.load( open( processed_text_filename, "rb" ) )
    else:
        sql = 'SELECT * FROM therapists'
        df = psql.sql_to_pandas(sql)
        top_n_percent_words = processor.get_top_n_percent_words(df[original_text_col],.1)
        custom_stop_words = ['selfesteem', 'cognitivebehavioral']
        additional_stops = top_n_percent_words + custom_stop_words
        df_processed = processor.processing_pipeline(df=df,text_col=original_text_col, min_doc_length= min_doc_length,
            additional_stop_words=additional_stops)
        print(df.head())
        pickle.dump(df_processed, open( processed_text_filename, "wb" ) )

    print(df_processed.head())

    # vis.word_distribution(df_processed)
    # vis.word_cloud(df_processed, process_text_col)
    # vis.ngram_bar_chart(df_processed[process_text_col],(1,1), 100)
    # vis.ngram_bar_chart(df_processed[process_text_col],(2,2), 20)

    tf_vectorizer = CountVectorizer(analyzer='word',
                            ngram_range=(2,2),
                            min_df=3,                       
                            stop_words=processor.get_stop_words(),                      
                            token_pattern='[a-zA-Z0-9]{3,}',  
                            max_features=5000,          
                            )

    tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())

    vectorizer = tfidf_vectorizer

    data_vectorized = vectorizer.fit_transform(df_processed['text_processed'])

    tm.run_lda(df_processed, process_text_col, vectorizer, data_vectorized)

    lda_model = LatentDirichletAllocation(n_components=15, # Number of topics
                                    learning_method='online',
                                    random_state=0,       
                                    n_jobs = -1  # Use all available CPUs
                                    )
    lda_model.fit(data_vectorized)

    df_topic_keywords = tm.show_topics(vectorizer=vectorizer, lda_model=lda_model, n_words=20)
    #print(df_topic_keywords)

    # topics_theme = ['Topic Theme 0', 'Topic Theme 1', 'Topic Theme 2', 'Topic Theme 3']
    # df_topic_keywords['topic_theme'] = topics_theme
    # df_topic_keywords.set_index('topic_theme', inplace=True)
    
    # print(df_topic_keywords.T)


    # doc_topic_matrix = lda_model.transform(data_vectorized)
    # # column names
    # topicnames = df_topic_keywords.T.columns

    # # index names
    # docnames = ["Doc" + str(i) for i in range(len(df_processed))]

    # # Make the pandas dataframe
    # df_document_topic = pd.DataFrame(np.round(doc_topic_matrix, 2), columns=topicnames, index=docnames)

    # # Get dominant topic for each document
    # dominant_topic = np.argmax(df_document_topic.values, axis=1)
    # df_document_topic['dominant_topic'] = dominant_topic

    # df_document_topic.reset_index(inplace=True)
    # df_sent_topic= pd.merge(df_processed, df_document_topic, left_index=True, right_index=True)
    # df_sent_topic.drop('index', axis=1, inplace=True)

    # df_topic_theme = df_sent_topic[['text_processed', 'dominant_topic']]

    # def label_theme(row):
    #     if row['dominant_topic'] == 0 :
    #         return topics_theme[0]
    #     if row['dominant_topic'] == 1 :
    #         return topics_theme[1]
    #     if row['dominant_topic'] == 2 :
    #         return topics_theme[2]
    #     if row['dominant_topic'] == 3:
    #         return topics_theme[3]
    #     if row['dominant_topic']  == 4:
    #         return topics_theme[4]
            
    # df_topic_theme['dominant_topic_theme'] = df_topic_theme.apply (lambda row: label_theme(row), axis=1)
    # print(df_topic_theme.head(15))

    vis = pyLDAvis.sklearn.prepare(lda_model, data_vectorized, vectorizer)

    pyLDAvis.save_html(vis, 'vis/ldavis_tfidf')