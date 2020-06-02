import pandas as pd
import numpy as np
from string import punctuation
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

import argparse

class NmfTopicModeler(object):
    def __init__(self, text_col):
        self.text_col = text_col

    def get_stop_words(self, new_stop_words=None):
        # Retrieve stop words and append any additional stop words
        stop_words = list(ENGLISH_STOP_WORDS)
        if new_stop_words:
            stop_words.extend(new_stop_words)
        return set(stop_words)

    def remove_punctuation(self, string, punc=punctuation):
        # remove given punctuation marks from a string
        for character in punc:
            string = string.replace(character,'')
        return string

    def lemmatize_str(self, string):
        # Lemmatize a string and return it in its original format
        w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
        lemmatizer = nltk.stem.WordNetLemmatizer()
        return " ".join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(string)])

    def clean_column(self, df, column, punctuation):
        # Apply data cleaning pipeline to a given pandas DataFrame column
        df[column] = df[column].apply(lambda x: str(x).lower())
        df[column] = df[column].apply(lambda x: self.remove_punctuation(x, punctuation))
        df[column] = df[column].apply(lambda x: self.lemmatize_str(x))
        return 

    def vectorize(self, df, stop_words):
        # Vectorize a text column of a pandas DataFrame
        text = df[self.text_col].values
        vectorizer = TfidfVectorizer(stop_words = stop_words) 
        X = vectorizer.fit_transform(text)
        features = np.array(vectorizer.get_feature_names())
        return X, features, vectorizer

    def get_nmf(self, X, n_components=7):
        # Create NMF matrixes based on a TF-IDF matrix
        nmf = NMF(n_components=n_components, max_iter=100, random_state=12345, alpha=0.5)
        W = nmf.fit_transform(X)
        H = nmf.components_
        return W, H, nmf
        
    def get_topic_words(self, H, features, n_features):
        # Retrieve feature names given H matrix, feature names, and number of features
        top_word_indexes = H.argsort()[:, ::-1][:,:n_features]
        return features[top_word_indexes]

    def print_topics(self, topics):
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
        
    def document_topics(self, W):
        return W.argsort()[:,::-1][:,0]
        
    def topic_counts(self, df):
        grouped = df[['topics',self.text_col]].groupby(['topics']).count().sort_values(by = self.text_col,ascending = False)
        print(tabulate(grouped, headers='keys', tablefmt='github'))

    def prepare_new_text(self, new_text:str):
        d = {self.text_col: [new_text]}
        df = pd.DataFrame(data=d)
        self.clean_column(df, self.text_col, punctuation)

        return df

    def classify_new_text(self, nmf_model, vectorizer, new_text:str):
        df = self.prepare_new_text(new_text)
        prepared_text = df[self.text_col].values
        X = vectorizer.transform(prepared_text)
        loadings = nmf_model.transform(X)

        return loadings

    def run_nmf(self, df):
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
            "zzz",
            "zzz"
        ]
        stop_words = self.get_stop_words(additional_stop_words)
        punc = punctuation
        n_topics = 17
        n_top_words = 10
        self.clean_column(df, text_col, punc)

        
        # vis.word_distribution(df)
        # vis.word_cloud(df, 'writing_sample')
        # vis.ngram_bar_chart(df['writing_sample'],(1,1), 100)
        # vis.ngram_bar_chart(df['writing_sample'],(2,2), 20) 

        X, features, vectorizer = self.vectorize(df, stop_words)
        W, H, nmf = self.get_nmf(X, n_components=n_topics)
        top_words = self.get_topic_words(H, features, n_features=n_top_words)
        df['topics'] = self.document_topics(W)
        #self.print_topics(top_words)
        self.print_topics(top_words.T)
        df.to_pickle("data/nmf_pickled_df")
        self.topic_counts(df)

        pickle.dump(nmf, open( 'models/nmf_model', "wb" ) )
        pickle.dump(vectorizer, open( 'models/nmf_vectorizer', "wb" ) )

        return nmf, vectorizer


if __name__ == '__main__':
    np.random.seed(10)
    #df = pd.read_pickle('data/df_processed_testing.pkl')
    psql = PostgreSQLHandler()
    vis = Visualizer(psql.get_conn())
    vis.set_show_figs(True)
    vis.set_save_figs(False)
    
    text_col = 'writing_sample'
    nmf_modeler = NmfTopicModeler(text_col)

    parser = argparse.ArgumentParser()
   
    parser.add_argument('-fd', '--fromdisk', action='store_true', 
        help="load model from local file")

    args = parser.parse_args()
    model = None
    model_filename = "models/nmf_model"
    if args.fromdisk:
        model = pickle.load( open( model_filename, "rb" ) )
        vectorizer = pickle.load( open( 'models/nmf_vectorizer', "rb" ) )
    else:
        sql = 'SELECT * FROM therapists'
        df = psql.sql_to_pandas(sql)

        

        model, vectorizer = nmf_modeler.run_nmf(df)

        pickle.dump(model, open( model_filename, "wb" ) )

    new_text = '''At a recovery meeting for loved ones, we focused on fear which can crush and overpower. Often we project worst-case scenarios. A litany of “what ifs” take over. We ruminate, we project, we worry. Our hearts sink when the phone rings in the middle of the night. Is our loved one in jail, or a car wreck, or a hospital emergency room? Because these heartbreaking events are often consequences of substance abuse, loved ones often stay on alert.
        Fear manifests in different ways. There’s fear of a tragic event, like a drug overdose, DUI, or suicide. And then there are less dramatic and more subtle worries. For example, when talking on the phone to my adult son who is in recovery, I pick up on his tone of voice. If it appears off kilter then "what ifs" take over. What if something bad is happening? What if he’s depressed? What if his depression triggers another episode of substance abuse? Although most parents pick up variations in their children’s tone of voice, I doubt that they jump to extreme conclusions. Rather, they might think that their loved one had a bad day or is tired or upset. More times than not this has been the case with my son. As Mark Twain said, “I’ve had a lot of worries in my life, most of which never happened.”
        But what if the worst thing did happen, then how do we deal with the fear that it will happen again? One way to break the cycle is to stay present. Easier said than done.  But when you think about it, all we have is the present moment. The past is over and the future doesn’t exist. Members in my recovery group have shared ways to stay present.  These include: meditation, prayer, gardening, cooking, painting, interacting with children, and volunteering. I’ve found that some of these suggestions have worked for me.  
        Recently I participated in a drawing class where I became singularly focused on drawing a simple ceramic bowl. Totally present for two hours: just me, a set of pencils, drawing paper, and that bowl. Swimming laps is another method I’ve found helpful. Stroke, breathe, kick….back and forth from one end of the pool to the other. I recently read a book by Andy Puddicombe, The Headspace Guide to Meditation and Mindfulness, How Mindfulness Can Change Your Life in Ten Minutes a Day.  It's helped motivate me to begin meditating on a regular basis. After all who can't find ten minutes a day to help become less anxious and sad? 
        The slogan “One Day at a Time”  reminds me to stay present.  It helps pull my attention away from projecting into the future and leaving yesterday's baggage behind. Similarly “Just for today” lightens my load of fear and worry. Another slogan, “Easy does it” reminds me to be gentle with myself when I revert to becoming anxious and fearful.  To quote Mark Twain again, “Courage is resistance to fear, mastery of fear, not the absence of fear.”
        '''

    print(nmf_modeler.classify_new_text(model, vectorizer, new_text))