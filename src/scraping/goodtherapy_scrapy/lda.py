import psycopg2
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from string import punctuation
import matplotlib.pyplot as plt
import datetime as dt

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from sklearn.decomposition import LatentDirichletAllocation

# see a 2d representation of the data using PCA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler(copy=True, with_mean=True, with_std=True)

class NlpProcessor(object):

    def __init__(self):
        self.conn = self.open_conn()

    def open_conn(self):
        return psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')

    def close_conn(self):
        self.conn = None

    def sql_to_pandas(self, sql:str)->pd.DataFrame:
        df = pd.read_sql_query(sql, self.conn)

        return df

    # tokenizing with nltk, with stemming/lemmatizing
    # this keeps punctuation
    def tokenize_doc(self, set_of_docs)->list:
        return [word_tokenize(content.lower()) for content in set_of_docs ]

    def remove_stopwords_and_punc(self, tokenized_set_of_docs:list, stop_words, remove_punc=True)->list:
        no_stops_docs = []
        for tokens in tokenized_set_of_docs:
            saved_tokens = []
            for token in tokens:
                if remove_punc:
                    if token.isalpha():
                        if token not in stop_words:
                            saved_tokens.append(token)
                else:
                    if token not in stop_words:
                        saved_tokens.append(token)
            no_stops_docs.append(saved_tokens)
            #no_stops_docs.append([word for word in words if word not in final_stop_words and word])
        
        return no_stops_docs

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

    def text_tokenization_pipeline(self, list_of_docs : list, stop_words, remove_punc : bool, tokenizer='wordnet') -> list:
        tokenized_docs = self.tokenize_doc(list_of_docs)
        no_stops_docs = self.remove_stopwords_and_punc(tokenized_docs, stop_words, remove_punc=remove_punc)
        lemm_stemm_docs = []
        if tokenizer == 'wordnet':
            lemm_stemm_docs = self.lemm_wordnet(no_stops_docs)
        elif tokenizer == 'porter':
            lemm_stemm_docs = self.stem_porter(no_stops_docs)
        elif tokenizer == 'snowball':
            lemm_stemm_docs = self.stem_snowball(no_stops_docs)
        else:
            lemm_stemm_docs = no_stops_docs
            
        return lemm_stemm_docs

    def remove_dupes_decorator(self, func):
        def func_wrapper(*args, **kwargs):
            dupes_removed_docs = func(*args, **kwargs)
            
            return [list(set(ls)) for ls in dupes_removed_docs]

        return func_wrapper

    def combine_stop_words(self, custom_stop_words:list)->list:
        stop_words = set(stopwords.words('english'))

        return stop_words.union(custom_stop_words)

    def create_term_freqeuncy_matrix(self, df:pd.DataFrame, all_stop_words:list, n_gram_range, max_features, remove_punc=True, tokenizer='None'):
        tokens = self.text_tokenization_pipeline(df['writing_sample'],stop_words=all_stop_words,
                                                remove_punc=True, tokenizer='none')

        documents = [' '.join(doc) for doc in tokens]

        # tfidf_vect = TfidfVectorizer(lowercase=False)
        # tfidf_matrix = tfidf_vect.fit_transform(documents)
        #print(tfidf_vect.get_feature_names())

        count_vect = CountVectorizer(max_features=max_features, ngram_range=n_gram_range)
        tf_matrix = count_vect.fit_transform(documents)

        return tf_matrix, count_vect

    def get_most_freq_words(self, count_vectorizer, tf_matrix, num_words, print_dict_to_terminal=False):
        top_words = []
        word_freqs = []
        
        word_list = count_vect.get_feature_names()
        count_list = tf_matrix.toarray().sum(axis=0)

        #combine these in a dictionary
        word_freq_dict = dict(zip(word_list, count_list))
        
        # dictionary.values() and .keys() return a view object, so we have to cast it to list in order to use it as desired
        for word_index in np.argsort(list(word_freq_dict.values()))[-num_words:]:
            top_words.append(list(word_freq_dict.keys())[word_index])
            word_freqs.append(list(word_freq_dict.values())[word_index])
            print('\n')
            if print_dict_to_terminal:
                print(f'{list(word_freq_dict.keys())[word_index]} : {list(word_freq_dict.values())[word_index]}')
            
        return top_words, word_freqs
        
    def display_topics(self, model, feature_names, num_top_n_grams, log=True)->None:
        topic_headers = []
        topic_n_grams = []
        for topic_idx, topic in enumerate(model.components_):
            topic_header = "Topic %d:" % (topic_idx)
            topic_ngram_list = " - ".join([feature_names[i]
                            for i in topic.argsort()[:-num_top_n_grams - 1:-1]])
            
            print(topic_header)
            topic_headers.append(topic_header)
            print(topic_ngram_list)
            topic_n_grams.append(topic_ngram_list)

        self.log_lda_results(model.get_params(), topic_headers, topic_n_grams)

    def log_lda_results(self, model_params:dict, topic_headers:list, topic_words_list:list)->None:
        file_log = open('../logs/lda_results_log.txt', 'a')
        breakpoint()
        header = '\n\n******************** LDA Results ********************'
        date_and_time = 'Timestamp: ' + str(dt.datetime.now())
        model_params_header = 'Model Parameters: \n-------------------------'
        params_s = ''
        for k, v in model_params.items():
            params_s += f'{k} : {v}\n'

        topics = ''
        for i, words in enumerate(topic_words_list):
            topics += f'Topic {i+1}\n\t{words}'

        L = [header, date_and_time, model_params_header, params_s, topics]

        for i in range(len(L)):
            L[i] += '\n'
        file_log.writelines(L)
        file_log.close()

if __name__ == '__main__':
    nlp = NlpProcessor()

    sql = "select * from therapists;"
    df = nlp.sql_to_pandas(sql)
    print(df.info())

    sql_age = 'SELECT * FROM age_groups;'
    sql_issues = 'SELECT  * FROM issues;'
    sql_orientations = 'SELECT * FROM orientations'
    sql_professions = 'SELECT * FROM professions'
    sql_services = 'SELECT * FROM services'

    df_age_groups = nlp.sql_to_pandas(sql_age)
    df_issues = nlp.sql_to_pandas(sql_issues)
    df_orientations = nlp.sql_to_pandas(sql_orientations)
    df_professions = nlp.sql_to_pandas(sql_professions)
    df_services = nlp.sql_to_pandas(sql_services)
    
    nlp.close_conn()

    custom_stop_words = ['change','family','find','approach','couples','issues','also',
    'anxiety','working','experience','relationship','relationships','therapist','counseling',
    'people','feel','clients','help','work','life','therapy','psychotherapy', 'feel', 
    'feeling','get', 'warson', 'counseling', 'way', 'practice']
    #custom_stop_words = []

    final_stop_words = nlp.combine_stop_words(custom_stop_words)

    tf_matrix, count_vect = nlp.create_term_freqeuncy_matrix(df=df, all_stop_words=final_stop_words, n_gram_range=(3,3), 
        max_features=1000, remove_punc=True, tokenizer='None')

    tf_feature_names = count_vect.get_feature_names()

    num_topics = 5
    lda = LatentDirichletAllocation(n_components=num_topics, learning_offset = 50., verbose=1,
                                    doc_topic_prior=1/num_topics, topic_word_prior= 1/num_topics,
                                    n_jobs=-1, learning_method = 'online',
                                    random_state=0)

    lda.fit(tf_matrix)

    num_top_n_grams = 10
    print(nlp.display_topics(lda, tf_feature_names, num_top_n_grams))
    print("\nModel perplexity: {0:0.3f}".format(lda.perplexity(tf_matrix)))
    
    words, counts = nlp.get_most_freq_words(count_vect, tf_matrix, 20, print_dict_to_terminal=True)