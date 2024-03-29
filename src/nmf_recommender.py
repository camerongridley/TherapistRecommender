import pandas as pd
import numpy as np
from string import punctuation
import nltk
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate
import matplotlib.pyplot as plt 

import pickle

class NmfRecommender(object):
    def __init__(self, text_col):
        self.text_col = text_col
        self.W = None
        self.H = None

    def get_stop_words(self, new_stop_words=None):
        '''Retrieve stop words and append any additional stop words'''
        stop_words = list(ENGLISH_STOP_WORDS)
        if new_stop_words:
            stop_words.extend(new_stop_words)
        return set(stop_words)

    def remove_punctuation(self, string, punc=punctuation):
        '''Remove given punctuation marks from a string'''
        for character in punc:
            string = string.replace(character,'')
        return string

    def lemmatize_str(self, string):
        '''Lemmatize a string and return it in its original format'''
        w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
        lemmatizer = nltk.stem.WordNetLemmatizer()
        return " ".join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(string)])

    def clean_column(self, df, column, punctuation):
        '''Apply data cleaning pipeline to a given pandas DataFrame column'''
        df[column] = df[column].apply(lambda x: str(x).lower())
        df[column] = df[column].apply(lambda x: self.remove_punctuation(x, punctuation))
        df[column] = df[column].apply(lambda x: self.lemmatize_str(x)) 
    
    def get_top_n_grams(self, corpus:pd.DataFrame, n_gram_range=(1,1), n=None, stop_words=None)->list:
        '''Returns tuple of ngram and corpus freqency'''
        vec = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit(corpus)
        # get tf matrix
        doc_term_mat = vec.transform(corpus)
        # sum all rows to get counts for each feature/word
        sum_words = doc_term_mat.sum(axis=0) 
        # make list of tuples that maps each sum to it's corresponding word using the vocabulary_ dictionary
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        # sort the list by word count, which is the second item in the tuple 
        words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
        
        return words_freq[:n]

    def add_most_freq_words_to_stops(self,df, stop_words, num_top_to_stop=0):
        '''Remove the specified number of most frequent words from the corpus and add them to stop words list'''
        most_freq_words = self.get_top_n_grams(df,(1,1), num_top_to_stop, stop_words)
        print(f'LEN OF TOP WORD LIST: {len(most_freq_words)}')
        stop_words = self.get_stop_words(most_freq_words)

    def vectorize(self, df, stop_words):
        '''Vectorize a text column of a pandas DataFrame'''
        text = df[self.text_col].values
        vectorizer = TfidfVectorizer(ngram_range=(2,2),stop_words = stop_words) 
        X = vectorizer.fit_transform(text)
        features = np.array(vectorizer.get_feature_names())
        return X, features, vectorizer

    def get_nmf(self, X, n_components=7):
        '''Create NMF matrixes based on a TF-IDF matrix'''
        nmf = NMF(n_components=n_components, max_iter=100, random_state=12345, alpha=0.5)
        W = nmf.fit_transform(X)
        H = nmf.components_
        self.W = W
        self.H = H
        return W, H, nmf
        
    def get_topic_words(self, H, features, n_features):
        '''Retrieve feature names given H matrix, feature names, and number of features'''
        top_word_indexes = H.argsort()[:, ::-1][:,:n_features]
        return features[top_word_indexes]

    def print_topics(self, topics, save_results=False):
        '''Print topics in markdown format'''
        n_words = len(topics[0])
        cols = ["Topic #"+ str(i) for i in range(n_words)]
        row_idx = [str(i) for i in range(len(topics))]
        df_pretty = pd.DataFrame(columns=cols)
        for topic in topics:
            df_pretty = df_pretty.append([dict(zip(cols, topic))])
        df_pretty['Word #'] = row_idx
        df_pretty = df_pretty.set_index('Word #')
        print(tabulate(df_pretty, headers='keys', tablefmt='github'))
        if save_results:
            self.write_html_file(df_pretty.to_html(), 'vis/topic_words.html')
        

    def write_html_file(self, html, filename):
        '''Save HTML file to disk'''
        html_file= open(filename,"w")
        html_file.write(html)
        html_file.close()

    def document_topics(self, W):
        '''Return document topics sorted by '''
        return W.argsort()[:,::-1][:,0]
        
    def topic_counts(self, df):
        '''Return count of docs per topic'''
        grouped = df[['dominant_topic',self.text_col]].groupby(['dominant_topic']).count().sort_values(by = self.text_col,ascending = False)
        print(tabulate(grouped, headers='keys', tablefmt='github'))

    def run_nmf(self, df, n_topics = 15, save_results=False):
        '''
        Clean and vectorize data in supplied DataFrame.
        Fit and transform NMF model with data.
        Pickle model if flagged.
        Return NMF model.
        '''
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
            "psychodynamic",
            "cognitive",
            "behavioral",
            "service",
            "hand",
            "furthermore",
            "suite",
            "arrange",
            "location",
            "2005",
            "health",
            "manhattan",
            "work",
            "working",
            "your",
            "dont",
            "youre",
            "people",
            "feel",
            "feeling",
            "want",
            "know",
            "way",
            "life",
            "good",
            "person",
            "come",
            "love",
            "my"
        ]
        stop_words = self.get_stop_words(additional_stop_words)
        punc = punctuation
        
        n_top_words = 10
        self.clean_column(df, self.text_col, punc)

        X, features, vectorizer = self.vectorize(df, stop_words)
        
        W, H, nmf = self.get_nmf(X, n_components=n_topics)
        top_words = self.get_topic_words(H, features, n_features=n_top_words)
        df['dominant_topic'] = self.document_topics(W)
        df['topic_weights'] = [x for x in W]
        #self.print_topics(top_words, save_results=False)
        self.print_topics(top_words.T, save_results=False)

        if save_results:
            df.to_pickle("data/nmf_pickled_df.pkl")
            pickle.dump(nmf, open( 'deploy/nmf_model.pkl', "wb" ) )
            pickle.dump(vectorizer, open( 'deploy/nmf_vectorizer.pkl', "wb" ) )
            pickle.dump(df, open( 'deploy/nmf_df_topics.pkl', "wb" ) )

        self.topic_counts(df)
        return nmf, vectorizer, df

    def classify_and_recommend(self, nmf_model:NMF, vectorizer:TfidfVectorizer, new_text:str,
        df_therapist_topics:pd.DataFrame, state:str, n_recs):
        '''Classify new text data and return recommendations for that text'''
        
        topic_loadings = self.classify_new_text(nmf_model, vectorizer, new_text)
        recs = self.make_recommendations(topic_loadings, df_therapist_topics, state, n_recs)

        return topic_loadings, recs

    def classify_new_text(self, nmf_model:NMF, vectorizer:TfidfVectorizer, new_text:str):
        '''Clean and fit new text data to the existing NMF model to determine the topics it contains.'''
        df = self.prepare_new_text(new_text)
        prepared_text = df[self.text_col].values
        X = vectorizer.transform(prepared_text)
        topic_loadings = nmf_model.transform(X)[0]
        
        updated_loadings = self.apply_topic_weighting(topic_loadings)

        dominant_topic_id = updated_loadings.argsort()[-1]
        
        return updated_loadings

    def prepare_new_text(self, new_text:str):
        '''Clean new text'''
        d = {self.text_col: [new_text]}
        df = pd.DataFrame(data=d)
        self.clean_column(df, self.text_col, punctuation)

        return df

    def apply_topic_weighting(self, topic_loadings:list)->list:
        '''Apply weights to topics'''
        #set all weights to 1
        topic_weights = np.ones(len(topic_loadings))
        #update desired indexes
        topic_weights[2] = .1 #Cost & Consultation topic
        topic_weights[7] = .1 # Insurance topic

        adjusted_topic_loadings = topic_weights * topic_loadings

        return adjusted_topic_loadings

    def make_recommendations(self, topic_loadings:list, df_therapist_topics:pd.DataFrame,
            state:str, n_recs):
        '''Return recommendations for topic loadings of new text'''
        
        #for col, val in filters.items():
        state_filter = df_therapist_topics['state'] == state
        filtered_df = df_therapist_topics[state_filter]

        filtered_df['cosine_sim'] = filtered_df['topic_weights'].apply(lambda x : cosine_similarity([topic_loadings], [x]))
        
        return filtered_df.sort_values(by=['cosine_sim'], ascending=False).head(n_recs)

    def get_dominant_topics(self, top_n_topics:int, topic_loadings:list):
        ''' Return dominant topic names for topic loadings of new text'''
        dominant_topic_ids = topic_loadings.argsort()[::-1][:top_n_topics] 

        return self.get_topic_names(dominant_topic_ids)

    def get_topic_names(self, topic_ids:list)->list:
        '''Topic names are defined here.
        Return list of topic names based on list of topic ids'''
        d = {
            0 : 'Office Environment',
            1 : 'Relational Conflict',
            2 : 'Cost and Consultation',
            3 : 'Experiential',
            4 : 'Diagnostic',
            5 : 'Primary Relationship Struggles',
            6 : 'Trauma',
            7 : 'Insurance',
            8 : 'Primary Family Struggles',
            9 : 'Professional Experience',
            10 : 'Eastern/Non-Traditional',
            11 : 'Emergencies',
            12 : 'Availiability',
            13 : 'Depression, Anxiety and Grief',
            14 : 'Safety and Comfort'
            
        }

        return [d.get(id) for id in topic_ids]

    def evaluate_n_topics(self, df:pd.DataFrame, min_topics:int, max_topics:int)->None:
        '''
        evaluates NMF model within specified range of topics using reconstruction error
        returns x array of topic number choice and y array of reconstruction error for corresponding topic num
        used for determining the number of topics to choose for NMF model
        '''
        
        x = np.arange(start=min_topics, stop=max_topics+1)
        y =[]#[self.get_nmf_reconstr_err(c, df) for c in x]

        for num in x:
            model, vectorizer, df_therapist_topics = self.run_nmf(df, num, save_results=False)
            y.append(model.reconstruction_err_)

        return x, y


if __name__ == '__main__':
    pass
