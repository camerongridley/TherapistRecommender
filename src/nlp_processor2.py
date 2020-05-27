import psycopg2
import numpy as np
import pandas as pd
from string import punctuation
from visualizer import Visualizer

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


if __name__ == '__main__':
    # instantiate nlp processor
    nlp = NlpProcessor(log_file_path='logs/lda_results_log.txt')
    
    # define colors for visualizations
    palette = ['#13bdb4','#80d090','#dad977','#e49046','#d43d51']
    vis = Visualizer(nlp.get_conn, palette)

    # connect to the database and load pandas dataframes
    sql = "select * from therapists;"
    df = nlp.sql_to_pandas(sql)
    
    

    # NLP analysis
    custom_stopwords = ['change','family','find','approach','couples','issues','also',
    'anxiety','working','experience','relationship','relationships','therapist','counseling',
    'people','feel','clients','help','work','life','therapy','psychotherapy', 'feel', 
    'feeling','get', 'warson', 'counseling', 'way', 'practice', 'call', 'today','health',
    'helping', 'free', 'depression', 'like', 'trauma', 'may', 'together', 'make',
    'process', 'want', 'support', 'believe', 'goal', 'one', 'session', 'time', 'offer',
    'individual', 'need', 'year', 'need', 'consultation', 'well', 'skill', 'new', 'emotional',
     'provide', 'take', 'use', 'goal', 'person', 'child', 'individual', 'life', 'many', 'healing',
      'problem', 'see', 'know']

    final_stop_words = nlp.combine_stop_words(custom_stopwords)

    tfidf_matrix, tfidf_vect = nlp.create_tf_idf_matrix(df['writing_sample'], all_stop_words=final_stop_words,max_feats=1000, 
        n_gram_range=(1,3), remove_punc=True, tokenizer='wordnet')

    tf_matrix, count_vect = nlp.create_tf_matrix(docs=df['writing_sample'], all_stop_words=final_stop_words, 
        n_gram_range=(1,1), max_features=1000, remove_punc=True, tokenizer='wordnet')

    selected_matrix = tfidf_matrix
    selected_vectorizer = tfidf_vect

    # vis.set_save_figs(False)
    vis.set_show_figs(True)

    # General EDA
    #nlp.run_initial_eda(vis, df)
    
    # PCA
    nlp.run_pca_tfidf(vis, tfidf_matrix)
    nlp.run_pca_tf(vis, tf_matrix)

    # LDA
    n_topics = 3
    lda = nlp.fit_lda_model(selected_matrix, num_topics=n_topics, alpha=1/n_topics, beta=1/n_topics)    
    num_top_n_grams = 10
    feature_names = selected_vectorizer.get_feature_names()
    nlp.display_topics(lda, feature_names, num_top_n_grams, custom_stopwords, log_lda=True)
    words, counts = nlp.get_most_freq_words(selected_vectorizer, selected_matrix, 20, print_dict_to_terminal=False)
    print('Most Frequent words/n_grams')
    print(words)
    print("Model perplexity: {0:0.3f}".format(lda.perplexity(selected_matrix)))
    
    nlp.close_conn()