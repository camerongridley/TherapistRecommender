import pandas as pd
import numpy as np
from string import punctuation
import json
from bs4 import BeautifulSoup
import nltk
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from tabulate import tabulate
import matplotlib.pyplot as plt 

import pickle

from topic_modeler import TopicModeler
from postgresql_handler import PostgreSQLHandler
from visualizer import Visualizer

def get_stop_words(new_stop_words=None):
    # Retrieve stop words and append any additional stop words
    stop_words = list(ENGLISH_STOP_WORDS)
    if new_stop_words:
        stop_words.extend(new_stop_words)
    return set(stop_words)

def remove_punctuation(string, punc=punctuation):
    # remove given punctuation marks from a string
    for character in punc:
        string = string.replace(character,'')
    return string

def lemmatize_str(string):
    # Lemmatize a string and return it in its original format
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(string)])

def clean_column(df, column, punctuation):
    # Apply data cleaning pipeline to a given pandas DataFrame column
    df[column] = df[column].apply(lambda x: str(x).lower())
    df[column] = df[column].apply(lambda x: remove_punctuation(x, punctuation))
    df[column] = df[column].apply(lambda x: lemmatize_str(x))
    return 

def vectorize(df, column, stop_words):
    # Vectorize a text column of a pandas DataFrame
    text = df[column].values
    vectorizer = TfidfVectorizer(stop_words = stop_words) 
    X = vectorizer.fit_transform(text)
    features = np.array(vectorizer.get_feature_names())
    return X, features, vectorizer

def get_nmf(X, n_components=7):
    # Create NMF matrixes based on a TF-IDF matrix
    nmf = NMF(n_components=n_components, max_iter=100, random_state=12345, alpha=0.0)
    W = nmf.fit_transform(X)
    H = nmf.components_
    return W, H, nmf
    
def get_topic_words(H, features, n_features):
    # Retrieve feature names given H matrix, feature names, and number of features
    top_word_indexes = H.argsort()[:, ::-1][:,:n_features]
    return features[top_word_indexes]

def print_topics(topics):
    # Print topics in markdown format
    n_words = len(topics[0])
    cols = ["Word #"+ str(i) for i in range(n_words)]
    row_idx = [str(i) for i in range(len(topics))]
    df_pretty = pd.DataFrame(columns=cols)
    for topic in topics:
        df_pretty = df_pretty.append([dict(zip(cols, topic))])
    df_pretty['Topic #'] = row_idx
    df_pretty = df_pretty.set_index('Topic #')
    print(tabulate(df_pretty, headers='keys', tablefmt='github'))
    return
    
def document_topics(W):
    return W.argsort()[:,::-1][:,0]
    
def topic_counts(df, text_col):
    grouped = df[['topics',text_col]].groupby(['topics']).count().sort_values(by = text_col,ascending = False)
    print(tabulate(grouped.head(), headers='keys', tablefmt='github'))
    
additional_stop_words = [
    "therapy",
    "therapist",
    "psychotherapy",
    "looking",
    "help",
    "douglas",
    "thing",
    "make",
    "just",
    "like",
    "time",
    "counseling",
    "zzz",
    "zzz"
]
if __name__ == '__main__':
    np.random.seed(10)
    #df = pd.read_pickle('data/df_processed_testing.pkl')
    psql = PostgreSQLHandler()
    vis = Visualizer(psql.get_conn())
    vis.set_show_figs(True)
    vis.set_save_figs(False)

    sql = 'SELECT * FROM therapists'
    df = psql.sql_to_pandas(sql)
    text_col = 'writing_sample'

    
    stop_words = get_stop_words(additional_stop_words)
    punc = punctuation
    n_topics = 4
    n_top_words = 10
    clean_column(df, text_col, punc)

    vis.word_distribution(df)
    vis.word_cloud(df, 'writing_sample')
    vis.ngram_bar_chart(df['writing_sample'],(1,1), 100)
    vis.ngram_bar_chart(df['writing_sample'],(2,2), 20)

    X, features, vectorizer = vectorize(df, text_col, stop_words)
    W, H, nmf = get_nmf(X, n_components=n_topics)
    top_words = get_topic_words(H, features, n_features=n_top_words)
    df['topics'] = document_topics(W)
    #print_topics(top_words)
    print_topics(top_words.T)
    df.to_pickle("data/nmf_pickled_df")
    topic_counts(df, text_col)

    pickle.dump(nmf, open( 'models/nmf_model', "wb" ) )

    # tm = TopicModeler(log_file_path='logs/lda_results_log.txt')

    # tm.run_lda(df, vectorizer, X)