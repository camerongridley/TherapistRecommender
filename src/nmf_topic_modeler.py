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

from topic_modeler import TopicModeler
from postgresql_handler import PostgreSQLHandler
from visualizer import Visualizer

import argparse

class NmfTopicModeler(object):
    def __init__(self, text_col):
        self.text_col = text_col
        self.W = None
        self.H = None

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
    
    
    def get_top_n_grams(self, corpus:pd.DataFrame, n_gram_range=(1,1), n=None, stop_words=None)->list:
        # returns tuple of ngram and corpus freqency
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
        most_freq_words = self.get_top_n_grams(df,(1,1), num_top_to_stop, stop_words)
        print(f'LEN OF TOP WORD LIST: {len(most_freq_words)}')
        stop_words = self.get_stop_words(most_freq_words)

    def vectorize(self, df, stop_words):
        # Vectorize a text column of a pandas DataFrame
        text = df[self.text_col].values
        vectorizer = TfidfVectorizer(ngram_range=(2,2),stop_words = stop_words) 
        X = vectorizer.fit_transform(text)
        features = np.array(vectorizer.get_feature_names())
        return X, features, vectorizer

    def get_nmf(self, X, n_components=7):
        # Create NMF matrixes based on a TF-IDF matrix
        nmf = NMF(n_components=n_components, max_iter=100, random_state=12345, alpha=0.5)
        W = nmf.fit_transform(X)
        H = nmf.components_
        self.W = W
        self.H = H
        return W, H, nmf
        
    def get_topic_words(self, H, features, n_features):
        # Retrieve feature names given H matrix, feature names, and number of features
        top_word_indexes = H.argsort()[:, ::-1][:,:n_features]
        return features[top_word_indexes]

    def print_topics(self, topics):
        # Print topics in markdown format
        n_words = len(topics[0])
        cols = ["Topic #"+ str(i) for i in range(n_words)]
        row_idx = [str(i) for i in range(len(topics))]
        df_pretty = pd.DataFrame(columns=cols)
        for topic in topics:
            df_pretty = df_pretty.append([dict(zip(cols, topic))])
        df_pretty['Word #'] = row_idx
        df_pretty = df_pretty.set_index('Word #')
        print(tabulate(df_pretty, headers='keys', tablefmt='github'))
        self.write_html_file(df_pretty.to_html(), 'vis/topic_words.html')
        
        return

    def write_html_file(self, html, filename):
        html_file= open(filename,"w")
        html_file.write(html)
        html_file.close()

    def document_topics(self, W):
        return W.argsort()[:,::-1][:,0]
        
    def topic_counts(self, df):
        grouped = df[['dominant_topic',self.text_col]].groupby(['dominant_topic']).count().sort_values(by = self.text_col,ascending = False)
        print(tabulate(grouped, headers='keys', tablefmt='github'))

    def run_nmf(self, df, n_topics = 15):
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
        self.clean_column(df, text_col, punc)

        X, features, vectorizer = self.vectorize(df, stop_words)
        W, H, nmf = self.get_nmf(X, n_components=n_topics)
        top_words = self.get_topic_words(H, features, n_features=n_top_words)
        df['dominant_topic'] = self.document_topics(W)
        df['topic_weights'] = [x for x in W]
        #self.print_topics(top_words)
        self.print_topics(top_words.T)
        df.to_pickle("data/nmf_pickled_df")
        self.topic_counts(df)

        pickle.dump(nmf, open( 'deploy/nmf_model', "wb" ) )
        pickle.dump(vectorizer, open( 'deploy/nmf_vectorizer', "wb" ) )
        pickle.dump(df, open( 'deploy/nmf_df_topics', "wb" ) )

        return nmf, vectorizer, df

    def prepare_new_text(self, new_text:str):
        d = {self.text_col: [new_text]}
        df = pd.DataFrame(data=d)
        self.clean_column(df, self.text_col, punctuation)

        return df

    def classify_new_text(self, nmf_model:NMF, vectorizer:TfidfVectorizer, new_text:str):
        df = self.prepare_new_text(new_text)
        prepared_text = df[self.text_col].values
        X = vectorizer.transform(prepared_text)
        loadings = nmf_model.transform(X)[0]
        dominant_topic = loadings.argsort()[-1]
        print(f'Dominant Topic: {dominant_topic}')
        return dominant_topic, loadings

    def make_recommendations(self, loadings:list, df_therapist_topics:pd.DataFrame,
            state:str, n_recs):
        
        #for col, val in filters.items():
        state_filter = df_therapist_topics['state'] == state
        filtered_df = df_therapist_topics[state_filter]

        filtered_df['cosine_sim'] = filtered_df['topic_weights'].apply(lambda x : cosine_similarity([loadings], [x]))
        # temporarily drop topics 4 and 6 from loadings for recommendations
        #filtered_df['cosine_sim'] = filtered_df['topic_weights'].apply(lambda x : cosine_similarity([np.delete(loadings,[4, 6])], [np.delete(x, [4,6])]))

        return filtered_df.sort_values(by=['cosine_sim'], ascending=False).head(n_recs)

    def classify_and_recommend(self, nmf_model:NMF, vectorizer:TfidfVectorizer, new_text:str,
        df_therapist_topics:pd.DataFrame, state:str, n_recs):
        
        dominant_topic, loadings = self.classify_new_text(model, vectorizer, new_text)
        return self.make_recommendations(loadings, df_therapist_topics, state, n_recs)

    def get_topic_names(self, topic_ids:list)->list:
        d = {
            0 : 'Office Environment',
            1 : 'Relational Conflict',
            2 : 'Cost and Consultation',
            3 : 'Experiential',
            4 : 'Diagnostic',
            5 : 'Primary Relationship Struggle',
            6 : 'Trauma',
            7 : 'Insurance',
            8 : 'Child and Aldolescence',
            9 : 'Professional Experience',
            10 : 'Eastern/Non-Traditional',
            11 : 'Emergencies',
            12 : 'Availiability',
            13 : 'Depression, Anxiety and Grief',
            14 : 'Safety and Comfort'
            
        }

        return [d.get(id) for id in topic_ids]

    def evaluate_n_topics(self, vis:Visualizer, df:pd.DataFrame, min_topics:int, max_topics:int)->None:
        
        x = np.arange(start=min_topics, stop=max_topics+1)
        y = [self.get_nmf_reconstr_err(c, df) for c in x]

        vis.make_plot(x=x, y=y, title='Reconstruction Error by Number of Topics', x_label='Number of Topics', y_label='Reconstruction Error')

    def get_nmf_reconstr_err(self, c, df):
        model, vectorizer, df_therapist_topics = self.run_nmf(df, c)
        return model.reconstruction_err_

if __name__ == '__main__':
    np.random.seed(10)
    
    text_col = 'writing_sample'
    nmf_modeler = NmfTopicModeler(text_col)

    parser = argparse.ArgumentParser()
   
    parser.add_argument('-fd', '--fromdisk', action='store_true', 
        help="load model with data from local file")

    parser.add_argument('-psql', '--frompsql', action='store_true', 
        help="load model with data from postgreSql database")

    args = parser.parse_args()
    model = None
    model_filename = "deploy/nmf_model"

    if args.frompsql:
        # dynamically created data, vectorizer and load data from postgreSQL database
        psql = PostgreSQLHandler()
        vis = Visualizer(psql.get_conn())
        vis.set_show_figs(True)
        vis.set_save_figs(True)
        
        sql = 'SELECT * FROM therapists'
        df = psql.sql_to_pandas(sql)

        model, vectorizer, df_therapist_topics = nmf_modeler.run_nmf(df=df, n_topics = 15)
        pickle.dump(model, open( model_filename, "wb" ) )

        # vis.word_distribution(df)
        # vis.word_cloud(df, 'writing_sample')
        # vis.ngram_bar_chart(df['writing_sample'],(1,1), 50)
        # vis.ngram_bar_chart(df['writing_sample'],(2,2), 20) 
        # vis.ngram_bar_chart(df['writing_sample'],(3,3), 20)

        #nmf_modeler.evaluate_n_topics(vis, df, 3, 40)

    else:
        # load data, vectorizer and model from local pickle files
        model = pickle.load( open( model_filename, "rb" ) )
        vectorizer = pickle.load( open( 'deploy/nmf_vectorizer', "rb" ) )
        df_therapist_topics = pickle.load( open( 'deploy/nmf_df_topics', "rb" ) )

    

    depression_text = '''I feel that I need to give a small explanation on the condition I suffer from before I get into my rant: I suffer from POTS, which if you've ever been severely dehydrated- it's those symptoms all the time. I get severe night sweats that make my room smell and soak my clothes, I can't control my temperature (I get painfully hot after showers, and unable to sweat), I CANNOT run up and down the stairs without my legs getting weak and wanting to collapse, I have to eat slowly, in small bites, and in small portions otherwise I feel like I can't breathe or might vomit, etc.

I used to be very active, I loved swimming though all I could do for the longest time was doggy paddle. I loved biking, I used to be able to bike for miles on vacations with my family. My dad and I would hike or walk along beaches and I'd pick rocks or shells. But after one particular abusive relationship I stopped all that. I became anorexic, barely maintaining 90 lbs. He said everything I did was wrong. I stopped singing, I stopped writing, I felt so useless, and he knew what he was doing. He said to me that he was "remaking me." In his eyes, he was trying to "fix" everything wrong with me. He'd hold me down despite being 3 times heavier than me, and I'd be hospitalized for trying to take my life or break up with him. I'd go to the hospital defending him and the bruises he gave me from it because it felt like he was all I had.

I know my grandparents (who adopted and raised me) love me and care for me, but their abusive behavior and narcissistic attitude makes it hard for me to reach out to them. Since him, I've never left the house. I was too afraid to make friends. Afraid of everything and everyone. My life is so different from then, and yet my mind is stuck there. I get into mind traps that I don't deserve the life I have. The small fuck ups I've made throughout, I have to repent for. I know I should go back to therapy. But, it's never made me want to die any less. Through all the talks I've been though and help I've received, I'm still struggling to even get started. I know how to help myself, that it's not going to be easy, and that getting out of this rut may take a long time, maybe even a few years, but I feel like an absolute failure. Age 20 and can't even work part time, and barely passed one class for college? Sure, I may have tried my hardest, but I feel like absolute shit. I don't have a will to live. My sole reason for still being here is for my fiance. I always say "at least I have him," and yet it's barely enough to keep me from choosing between him and dying. I know he's scared that one day I'll just snap- he keeps promising he'll get me out of here, we'll live together, and everything will get better in our own time, but I can barely remember or put the effort to care for myself. I don't want to drag him down with me. But there's always a little voice in my head telling me that as soon as I start to care for myself that I'll fail or still be a failure.

My medical condition has only given me one solace: brain fog. My depression and the brain fog from my POTS practically make me an amnesiac. It's the only thing that gets me through a day anymore. On days when I do remember everything I'm so miserable that all I can do is shake, wail, and cry. I don't want to be this way. I want to want life, and even though I've been only surrounding myself with positivity, I can't make myself want to live.

I only have a few wishes. I wish I had the will to live- to fight for my life- to do something for myself that isn't just temporary self-indulgence. I wish I can experience the future with my fiance, whatever that may mean. But with how things are in my life, how I feel, how little I've been doing with my life- I feel like I deserve my condition. Isolated.'''

    ptsd_text = '''Although I have been healing for the past two years with lot of therapy and self care . I don’t feel “normal” . I am not the same person as I was when I was 18 . It is frustrating and sometimes causes me to unable to do things I really want to do . For example , I want to date people and experience more sex but I can’t bring myself to do it . Every time I have feelings for someone , I ended up telling myself that I don’t deserve to be with that person because for years , I have convinced myself that I am “broken “ . I feel that a lot of my experiences to explore more of my sexuality and sex was robbed by a traumatic event I had when I was eighteen . I ran away from it by joining a Christian campus group which I regret deeply . I was even more further shamed for my sexuality and a desire to have sex . Thankfully , I left that fucking group ,later joined a university in a diverse city after I graduated from a community college . I am super happy that I did because I finally was able to learn what an healthy sex life looks like . I had feelings for several people but was unable to tell them . I even joined tinder and met some people but I freaked out and stop responding to people that I was interested in dating ( I know it is a dick move, I was paralyzed with fear . I still feel guilty about it ) . I want to stop being paranoid about people but honestly it really because I don’t trust myself sometimes . I fucking hate it . I hate that it made me feel invalidated. I have this stupid fear that people wouldn’t want to be with me because I haven’t have a lot of experience in having sex. I am 27 now and I haven’t been in relationships or have sex or dated . What is wrong with me ?'''

    addiction_text = '''So, since I moved to another European country around 5 years ago, I started to get into doing cocaine at the weekends. This went from the odd weekend, to almost every weekend, and when I met my current partner (who is an addict and has been to rehab) and we started doing it more together, it went from weekends to the odd weekday. Of late it has been much better than it was, especially after a few really bad, scary comedowns (he's had heart issues because of his addiction, and seeing him clutching his chest was enough for us to stop for a few measly weeks). Then lockdown happened and it was the perfect opportunity for us to escape it...and we did, until the lockdown was lifted and we socialised and we were amongst our circle of friends who all do it, too. Since that day, not so long ago, I have woke up craving most days. I went out for dinner recently and had two drinks and got some because I felt I had to. I came home high and got high all night secretly without my partner knowing. The next day we spent the day together and I was high then, too. He noticed and got really angry, as he should have. He sees a clean road ahead and wants to stop. He has for a while. Last night we had an argument, I went out, had a drink and got high. It's any excuse, really. Even now I am home alone and I want to get some.

So my question is, am I an addict? Have I crossed the line? Am I no longer just a recreational user? What's my next move?'''

    marriage_text = '''Been married 5 years now. Met my wife 6 months before we got married. My first, her 4th. For the first 2-3 years I felt she was trying to control me. Always a killjoy whenever Id be adventurous or just have fun(simple things, like singing to the radio), always suspicious of other women(I've never cheated on anyone or come close), constantly accusing me of infidelity. Demanding of my time. Fights to be in control of the money, even when I was the only source of income.

After 2-3 years we had a big fight and I finally cornered her on all the unjust treatment and called her a control freak and she admitted it fully.

I am not completely innocent of course but, I have always been as honest as possible. Even when it gets me in trouble. This destroyed my trust for her. All this time in my own mind defending her. Telling myself she had honest intentions and that it was my fault. And then realizing she was manipulative. I can't seem to get over this.

All intimacy has died. Sex is a chore. We separated temporarily a few times but we keep deciding to try and make it work.

We're having trouble now again. I thought we could build the relationship up but she is averse to therapy. Feels like we are both unhappy and treading water. We're not building any noticeable trust, just trying not to fight.

Not sure what to do.''' 

    state = 'California'
    n_recs = 5
    dominant_topic, loadings = nmf_modeler.classify_new_text(model, vectorizer, depression_text)
    print(f'depression_text - dominant topic: {nmf_modeler.get_topic_names([dominant_topic])} -- loadings: {loadings}')
    recs = nmf_modeler.make_recommendations(loadings, df_therapist_topics, state, n_recs)
    print(f'\nRecs:\n{recs}\n')
    nmf_modeler.write_html_file(recs[['first_name', 'last_name', 'website', 'phone']].to_html(), 'img/testing/recs.html')

    dominant_topic, loadings = nmf_modeler.classify_new_text(model, vectorizer, ptsd_text)
    print(f'ptsd_text - dominant topic: {nmf_modeler.get_topic_names([dominant_topic])} -- loadings: {loadings}')
    print(f'\nRecs:\n{nmf_modeler.make_recommendations(loadings, df_therapist_topics, state, n_recs)}\n')

    dominant_topic, loadings = nmf_modeler.classify_new_text(model, vectorizer, addiction_text)
    print(f'addiction_text - dominant topic: {nmf_modeler.get_topic_names([dominant_topic])} -- loadings: {loadings}')
    print(f'\nRecs:\n{nmf_modeler.make_recommendations(loadings, df_therapist_topics, state, n_recs)}\n')

    dominant_topic, loadings = nmf_modeler.classify_new_text(model, vectorizer, marriage_text)
    print(f'marriage_text - dominant topic: {nmf_modeler.get_topic_names([dominant_topic])} -- loadings: {loadings}')
    print(f'\nRecs:\n{nmf_modeler.make_recommendations(loadings, df_therapist_topics, state, n_recs)}\n')

    #print(f'\nRecs:\n{nmf_modeler.make_recommendations(loadings, df_therapist_topics, "Denver", 5)}')

    #print(f'\nRecs:\n{nmf_modeler.classify_and_recommend(model, vectorizer, new_text, df_therapist_topics, "Denver", 10)}')