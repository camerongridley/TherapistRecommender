import psycopg2
import numpy as np
import pandas as pd
from string import punctuation
import datetime as dt
from visualizer import Visualizer


from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
#from nltk.corpus import stopwords

import pyLDAvis
import pyLDAvis.sklearn

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px

scaler = StandardScaler(copy=True, with_mean=True, with_std=True)

class NlpProcessor(object):

    def __init__(self, log_file_path):
        self.conn = self.open_conn()
        self.log_file_path = log_file_path

    def open_conn(self):
        return psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')

    def get_conn(self):
        return self.conn

    def close_conn(self):
        self.conn = None

    def sql_to_pandas(self, sql:str)->pd.DataFrame:
        df = pd.read_sql_query(sql, self.conn)

        return df

    # tokenizing with nltk, with stemming/lemmatizing
    # this keeps punctuation
    def tokenize_doc(self, set_of_docs)->list:
        return [word_tokenize(content.lower()) for content in set_of_docs ]

    def remove_punc(self, tokenized_set_of_docs:list)->list:
        no_punc_docs = []
        for tokens in tokenized_set_of_docs:
            saved_tokens = []
            for token in tokens:
                if token.isalpha():
                    saved_tokens.append(token)

            no_punc_docs.append(saved_tokens)
        
        return no_punc_docs

    def stem_porter(self, tokenized_set_of_docs:list)->list:
        porter = PorterStemmer()
        porter_docs = []
        for words in tokenized_set_of_docs:
            porter_docs.append([porter.stem(word) for word in words])
        
        return porter_docs

    def stem_snowball(self, tokenized_set_of_docs:list)->list:
        snowball = SnowballStemmer('english')
        snowball_docs = []
        for words in tokenized_set_of_docs:
            snowball_docs.append([snowball.stem(word) for word in words])
        
        return snowball_docs

    def lemm_wordnet(self, tokenized_set_of_docs:list)->list:
        wordnet = WordNetLemmatizer()
        wordnet_docs = []
        for words in tokenized_set_of_docs:
            wordnet_docs.append([wordnet.lemmatize(word) for word in words])
        
        return wordnet_docs

    def text_tokenization_pipeline(self, list_of_docs : list, remove_punc : bool, tokenizer='wordnet') -> list:
        tokenized_docs = self.tokenize_doc(list_of_docs)
        if remove_punc:
            updated_docs = self.remove_punc(tokenized_docs)
        else:
            updated_docs = tokenized_docs

        lemm_stemm_docs = []
        if tokenizer == 'wordnet':
            lemm_stemm_docs = self.lemm_wordnet(updated_docs)
        elif tokenizer == 'porter':
            lemm_stemm_docs = self.stem_porter(updated_docs)
        elif tokenizer == 'snowball':
            lemm_stemm_docs = self.stem_snowball(updated_docs)
        else:
            lemm_stemm_docs = updated_docs
            
        return lemm_stemm_docs

    def combine_stop_words(self, custom_stop_words:list)->list:
        stop_words = list(set(custom_stop_words))
        stop_words = stop_words + stopwords.words('english')

        return stop_words

    def create_tf_matrix(self, docs, all_stop_words:list, n_gram_range, max_features, remove_punc=True, tokenizer='None'):
        tokens = self.text_tokenization_pipeline(docs, remove_punc=True, tokenizer=tokenizer)

        documents = [' '.join(doc) for doc in tokens]

        count_vect = CountVectorizer(max_features=max_features, ngram_range=n_gram_range, lowercase=True, stop_words=all_stop_words)
        tf_matrix = count_vect.fit_transform(documents)

        return tf_matrix, count_vect

    def create_tf_idf_matrix(self, docs, all_stop_words:list, max_feats, n_gram_range, remove_punc=True, tokenizer='None'):
        # tokens is a list of lists - words per document
        tokens = self.text_tokenization_pipeline(docs, remove_punc=remove_punc, tokenizer=tokenizer)

        # reconstruct each document after processing
        documents = [' '.join(doc) for doc in tokens]
        tfidf_vect = TfidfVectorizer(ngram_range=n_gram_range,max_features=max_feats, lowercase=True, stop_words=all_stop_words)
        tfidf_matrix = tfidf_vect.fit_transform(documents)
        #print(tfidf_vect.get_feature_names())
        
        return tfidf_matrix, tfidf_vect

    def get_most_freq_words(self, vectorizer, X_matrix, num_words, print_dict_to_terminal=False):
        top_words = []
        word_freqs = []
        
        word_list = vectorizer.get_feature_names()
        count_list = X_matrix.toarray().sum(axis=0)

        #combine these in a dictionary
        word_freq_dict = dict(zip(word_list, count_list))
        
        # dictionary.values() and .keys() return a view object, so we have to cast it to list in order to use it as desired
        for word_index in np.argsort(list(word_freq_dict.values()))[-num_words:]:
            top_words.append(list(word_freq_dict.keys())[word_index])
            word_freqs.append(list(word_freq_dict.values())[word_index])
            if print_dict_to_terminal:
                print(f'{list(word_freq_dict.keys())[word_index]} : {list(word_freq_dict.values())[word_index]}')
            
        return top_words, word_freqs
        
    def display_topics(self, model, feature_names, num_top_n_grams, custom_stopwords, log_lda=False)->None:
        topic_ngram_dict = {}

        for topic_idx, topic in enumerate(model.components_):
            topic_header = "Topic %d:" % (topic_idx)
            print(topic_header)
            single_topic_n_grams = []
            for i in topic.argsort()[:-num_top_n_grams - 1:-1]:
                single_topic_n_grams.append(feature_names[i]) 

            print(single_topic_n_grams)
            topic_ngram_dict[topic_idx] = single_topic_n_grams
        if log_lda:
            self.log_lda_results(model, topic_ngram_dict, custom_stopwords)

    def log_lda_results(self, model, topic_ngram_dict:dict, custom_stopwords:list)->None:
        file_log = open(self.log_file_path, 'a')
        model_params = model.get_params()
        header = '\n\n**************************************** LDA Results ****************************************'
        date_and_time = 'Timestamp: ' + str(dt.datetime.now())
        model_params_header = '\nModel Parameters: \n-------------------------'
        params_str = ''
        for k, v in model_params.items():
            params_str += f'{k} : {v}\n'

        perplex = 'N/A'#"Model perplexity: {0:0.3f}".format(lda.perplexity(tf_matrix)) + '\n'

        stopwords_header = 'Stop words used:'
        stopwords_str = ', '.join([stop for stop in custom_stopwords])
        stopwords_str += '\n'

        L = [header, date_and_time, model_params_header, params_str, perplex, stopwords_header, stopwords_str]

        for topic_idx, n_gram_list in topic_ngram_dict.items():
            L.append(f'Topic: {str(topic_idx)}\n\t{", ".join([ng for ng in n_gram_list])}')

        for i in range(len(L)):
            L[i] += '\n'
        file_log.writelines(L)
        file_log.close()

    def run_pca_tfidf(self, vis, tfidf_matrix):
        # PCA with TFIDF
        X_tfidf_scaled = scaler.fit_transform(tfidf_matrix.todense()) # standardize data

        # Just 2 components - see any sig change between component 1 and 2? Hopefully!
        pca_tfidf = PCA(n_components=2) 
        X_pca_tfidf = pca_tfidf.fit_transform(X_tfidf_scaled) 
        vis.plot_2_pca_comps(X_pca_tfidf, title_suffix='with TFIDF Matrix', filename_suffix='tfidf')
        
        # How many components will explain enough variance?
        pca_tfidf = PCA()
        pca_tfidf.fit(X_tfidf_scaled)
        vis.cum_scree_plot(pca_tfidf, title='Cumulative Variance Explained using TF-IDF Matrix', filename_suffix='tfidf')

    def run_pca_tf(self, vis, tf_matrix):
        # PCA with TF
        X_tf_scaled = scaler.fit_transform(tf_matrix.todense()) # standardize data

        # with just 2
        pca_tf = PCA(n_components=2)
        X_pca_tf = pca_tf.fit_transform(X_tf_scaled)
        vis.plot_2_pca_comps(X_pca_tf, title_suffix='with TF Matrix', filename_suffix='tf')

        # How many components will explain enough variance?
        pca_tf = PCA()
        pca_tf.fit(X_tf_scaled)
        vis.cum_scree_plot(pca_tf, title='Cumulative Variance Explained using TF Matrix', filename_suffix='tf')

    def run_initial_eda(self, visualizer, df):
        # number of unique values per category
        sql_age = 'SELECT * FROM age_groups;'
        sql_issues = 'SELECT  * FROM issues;'
        sql_orientations = 'SELECT * FROM orientations'
        sql_professions = 'SELECT * FROM professions'
        sql_services = 'SELECT * FROM services'

        df_age_groups = self.sql_to_pandas(sql_age)
        df_issues = self.sql_to_pandas(sql_issues)
        df_orientations = self.sql_to_pandas(sql_orientations)
        df_professions = self.sql_to_pandas(sql_professions)
        df_services = self.sql_to_pandas(sql_services)

        visualizer.run_initial_eda_charts(df, df_age_groups, df_issues, 
            df_orientations, df_professions, df_services)

    def fit_lda_model(self, X_matrix, num_topics=5, alpha=.2 , beta=.2):
        lda = LatentDirichletAllocation(n_components=num_topics, learning_offset = 50., verbose=1,
                                        doc_topic_prior=alpha, topic_word_prior= beta,
                                        n_jobs=-1, learning_method = 'online',
                                        random_state=0)

        lda.fit(X_matrix)

        return lda


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