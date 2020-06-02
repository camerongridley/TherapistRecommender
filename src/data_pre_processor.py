import numpy as np
import pandas as pd
from string import punctuation
from postgresql_handler import PostgreSQLHandler
from spacy.lang.en.stop_words import STOP_WORDS as spacy_stops
from sklearn.feature_extraction.text import CountVectorizer

import re, nltk, spacy, string

from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

import argparse

class DataPreProcessor(object):
    def __init__(self):
        self.nlp = spacy.load("en")
        self.all_stop_words = spacy_stops
        self.custom_stop_words = None

    def add_stop_words(self, custom_stops:list)->None:
        self.nlp.Defaults.stop_words |= set(custom_stops)
        #self.all_stop_words = list(set(list(self.all_stop_words) + custom_stops))

    def get_stop_words(self):
        return spacy_stops

    # returns tuple of ngram and corpus freqency
    def get_top_n_grams(self, corpus:pd.DataFrame, n_gram_range=(1,1), n=None, stop_words=spacy_stops)->list:
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

    def get_top_n_percent_words(self, corpus:pd.DataFrame, n_percent:float, stop_words=spacy_stops)->list:
        words_freq = self.get_top_n_grams(corpus, (1,1))
        cutoff = int(len(words_freq) * n_percent)
        top_words = [x[0] for x in words_freq[: cutoff]]

        return top_words

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
            text = re.sub(r'[%s]' % re.escape(punctuation), ' ', text)

        # remove newline and return characters
        text = re.sub(r'[%s]' % re.escape('\n'), ' ', text)
        text = re.sub(r'[%s]' % re.escape('\r'), ' ', text)

        return text

    def remove_stop_words(self, nlp, text):
        doc = nlp(text)

        # Create list of word tokens
        token_list = []
        for token in doc:
            token_list.append(token.text)

        # Create list of word tokens after removing stopwords
        filtered_text =[] 

        for word in token_list:
            lexeme = nlp.vocab[word]
            if lexeme.is_stop == False:
                filtered_text.append(word)

        return ' '.join(filtered_text)

    # lemmatize with spaCy
    def spacy_lemmatize(self, nlp, text:str, remove_stops=True)->str:
        lemmed = []
        doc = nlp(text)

        for word in doc:
            if remove_stops:
                if word.is_stop == False:
                    lemmed.append(word.lemma_)
            else:
                lemmed.append(word.lemma_)
        
        return ' '.join(lemmed)

    def wordnet_lemmatize(self, text:str, remove_stops=True)->list:
        tokenized_text = word_tokenize(text)
        wordnet = WordNetLemmatizer()
        wordnet_docs = []

        for token in tokenized_text:
            if remove_stops:
                if token.is_stop == False:
                    wordnet_docs.append(wordnet.lemmatize(token))
            else:
                wordnet_docs.append(wordnet.lemmatize(token))
        wordnet_docs.append([wordnet.lemmatize(word) for word in tokenized_text])
        
        return wordnet_docs

    def processing_pipeline(self, df:pd.DataFrame, text_col:str, min_doc_length:int, additional_stop_words:list=None)->pd.DataFrame:
        df_clean = self.drop_short_docs(df ,text_col, min_doc_length)
        # initial text cleaning
        df_clean['text_processed'] = pd.DataFrame(df_clean[text_col].apply(lambda x: self.clean_text(x)))
        # update additional stop words supplied
        self.add_stop_words(additional_stop_words)
        # lemmatize and remove stop words with spaCy
        df_clean['text_processed'] = df_clean.apply(lambda x: self.spacy_lemmatize(nlp=self.nlp, text=x['text_processed'], 
                remove_stops=True), axis=1)
        # df_clean['writing_sample_processed'] = df_clean.apply(lambda x: self.wordnet_lemmatize(text=x['text_processed'], 
        #         remove_stops=True), axis=1)
        # remove spaCy -PRON-
        df_clean['text_processed'] = df_clean['text_processed'].str.replace('-PRON-', '')

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
        
        df_processed = processor.processing_pipeline(df,'writing_sample', 200)
        print(df.head())
        pickle.dump(df_processed, open( 'data/df_processed_testing.pkl', "wb" ) )

    print(df_processed.head())

    #vis.word_distribution(df_processed)
    #vis.word_cloud(df_processed, 'writing_sample_processed')
    #vis.ngram_bar_chart(df_processed['writing_sample_processed'],(1,1), 40)
    #vis.ngram_bar_chart(df_processed['writing_sample_processed'],(4,4), 20)

    psql.close_conn()


    