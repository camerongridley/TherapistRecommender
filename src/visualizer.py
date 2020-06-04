import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from spacy.lang.en.stop_words import STOP_WORDS as spacy_stops

import pyLDAvis
import pyLDAvis.sklearn

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px

from sklearn.feature_extraction.text import CountVectorizer

from data_pre_processor import DataPreProcessor

plt.rcParams['font.family'] = 'Ubuntu'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['font.size'] = 18
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

plt.rcParams['xtick.major.size'] = 10
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 2
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['figure.figsize'] = [10,6]
#plt.rcParams['savefig.dpi']=300

class Visualizer(object):

    def __init__(self, conn, palette = ['#13bdb4','#80d090','#dad977','#e49046','#d43d51']):
        self.conn = conn
        self.save_figs = False
        self.show_figs = False
        self.palette = palette
        self.visualiztion_directory = 'img/testing/'

    def sql_to_pandas(self, sql:str)->pd.DataFrame:
        df = pd.read_sql_query(sql, self.conn)

        return df

    def set_save_figs(self, choice:bool)->None:
        self.save_figs = choice

    def set_show_figs(self, choice:bool)->None:
        self.show_figs = choice

    def plot_2_pca_comps(self, X_pca:np.ndarray, title_suffix='', filename_suffix='')->None:
        fig, ax = plt.subplots(1, 1)
        ax.scatter(X_pca[:, 0], X_pca[:, 1],
                cmap=plt.cm.Set1, edgecolor='k', s=40)
        ax.set_title(f'First two PCA directions {title_suffix}')
        ax.set_xlabel("1st eigenvector (PC1)")
        ax.set_ylabel("2nd eigenvector (PC2)")
        plt.tight_layout()
        if self.save_figs:
            plt.savefig(f'{self.visualiztion_directory}data_vis/pca_2_comps_{filename_suffix}.png')
        if self.show_figs:
            plt.show()

    def scree_plot(self, pca:np.ndarray, title='', filename_suffix='')->None:
        # plot explained variance ratio in a scree plot
        plt.figure(1)
        plt.clf()
        plt.axes([.2, .2, .7, .7])
        plt.plot(pca.explained_variance_, linewidth=2, color=self.palette[0])
        plt.axis('tight')
        plt.xlabel('n_components')
        plt.ylabel('explained_variance_')
        plt.title(title)
        plt.tight_layout()
        if self.save_figs:
            plt.savefig(f'{self.visualiztion_directory}data_vis/pca_scree_{filename_suffix}.png')
        if self.show_figs:
            plt.show()
    
    def cum_scree_plot(self, pca:np.ndarray, title='', filename_suffix='')->None:
        total_variance = np.sum(pca.explained_variance_)
        cum_variance = np.cumsum(pca.explained_variance_)
        prop_var_expl = cum_variance/total_variance

        fig, ax = plt.subplots()
        ax.plot(prop_var_expl, color=self.palette[0], linewidth=2, label='Explained variance')
        ax.axhline(0.9, label='90% goal', linestyle='--', color=self.palette[3], linewidth=1)
        ax.set_ylabel('cumulative prop. of explained variance')
        ax.set_xlabel('number of principal components')
        plt.title(title)
        ax.legend()
        plt.tight_layout()
        if self.save_figs:
            plt.savefig(f'{self.visualiztion_directory}data_vis/pca_cum_scree_{filename_suffix}.png')
        if self.show_figs:
            plt.show()

    def word_distribution(self, df:pd.DataFrame)->None:
        # word length histogram
        writing_lengths = []
        for body in df['writing_sample']:
            writing_lengths.append(len(body))
            
        writing_lengths.sort()

        mean = np.mean(writing_lengths)
        mean_label = f'Mean: {np.around(mean, decimals=0)}'
        c1 = self.palette[0]
        c2 = self.palette[4]
        fig, ax = plt.subplots()
        ax.set_xlabel('Word Count')
        ax.set_ylabel('Therapists')
        ax.set_title('Practice Description Word Counts')
        ax.hist(writing_lengths, bins=100, color=c1)
        ax.axvline(x=mean, c=c2)
        plt.text(mean+200, 422, mean_label, bbox=dict(facecolor=c2, alpha=0.5))
        if self.save_figs:
            plt.savefig(f'{self.visualiztion_directory}design/word_count_hist.png')
        if self.show_figs:
            plt.show()

    def unique_categories_bar(self, df_age_groups:pd.DataFrame, df_issues:pd.DataFrame, 
        df_orientations:pd.DataFrame, df_professions:pd.DataFrame, df_services:pd.DataFrame)->None:
        age_groups_unique_size = df_age_groups['age_group'].unique().size
        issues_unique_size = df_issues['issue'].unique().size
        orientations_unique_size = df_orientations['orientation'].unique().size
        professions_unique_size = df_professions['profession'].unique().size
        service_unique_size = df_services['service'].unique().size

        heights = [age_groups_unique_size, issues_unique_size, orientations_unique_size,
           professions_unique_size, service_unique_size]
        labels = ['age groups', 'issues', 'orientations', 'professions', 'services']
        colors = [self.palette[i] for i in range(len(heights))]

        fig, ax = plt.subplots()
        ax.set_title('Unique Entries for Profile Categories')
        ax.set_ylabel('Number of Unique Entries')
        ax.bar(height = heights, x=labels, color=colors)
        if self.save_figs:
            plt.savefig(f'{self.visualiztion_directory}design/uniques_per_category.png')

    def run_initial_eda_charts(self, df:pd.DataFrame, df_age_groups:pd.DataFrame, df_issues:pd.DataFrame, 
        df_orientations:pd.DataFrame, df_professions:pd.DataFrame, df_services:pd.DataFrame)->None:

        # word length histogram
        self.word_distribution(df)

        # unique categories bar chart
        self.unique_categories_bar(df_age_groups, df_issues, 
            df_orientations, df_professions, df_services)

        # # has website bar chart
        # mask_no_website = df['website']=='None'
        # height = [df[~mask_no_website]['website'].size, df[mask_no_website]['website'].size]
        # labels = ['Website', 'No Website']

        # c = [self.palette[0], self.palette[3]]
        # fig, ax = plt.subplots()
        # ax.bar(labels, height, color=c)
        # ax.set_ylabel('Num. of Therapists')
        # ax.set_title("Therapists with Websites")
        # if self.save_figs:
        #     plt.savefig(f'{self.visualiztion_directory}design/website_bar.png')

    def word_cloud(self, df:pd.DataFrame, col_name:str, max_words=500)->None:
        #stopwords = set(stop_words)

        text = str(df[col_name])
        # clean_text = [word for word in text.split() if word not in stop_words]
        # text = ' '.join([str(elem) for elem in clean_text])
        wordcloud = WordCloud(width=1600, height=800, 
        background_color='white').generate(text)
        # Open a plot of the generated image.

        plt.figure( figsize=(20,10), facecolor='k')
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)

        if self.save_figs:
            plt.savefig(f'{self.visualiztion_directory}data_vis/word_cloud.png')

        plt.show()
        # wordcloud = WordCloud(
        #     width=1600, height=800,
        #     background_color='white',
        #     stopwords = stopwords,
        #     max_words = max_words,
        #     max_font_size = 40,
        #     random_state = 42,
        #     interpolation="bilinear"
        # ).generate(str(df[col_name]))

        # print(wordcloud)
        # fig = plt.figure(1, dpi=200, figsize=(20, 10))
        # plt.imshow(wordcloud)
        # plt.axis('off')
        # plt.show()
        

    # # returns tuple of ngram and corpus freqency
    # def get_top_n_grams(self, corpus:pd.DataFrame, n_gram_range=(1,1), n=None, stopwords=spacy_stops)->list:
    #     vec = CountVectorizer(ngram_range=n_gram_range, stop_words=stopwords).fit(corpus)
    #     # get tf matrix
    #     doc_term_mat = vec.transform(corpus)
    #     # sum all rows to get counts for each feature/word
    #     sum_words = doc_term_mat.sum(axis=0) 
    #     # make list of tuples that maps each sum to it's corresponding word using the vocabulary_ dictionary
    #     words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    #     # sort the list by word count, which is the second item in the tuple 
    #     words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
        
    #     return words_freq[:n]

    def ngram_bar_chart(self, corpus:pd.DataFrame, n_gram_range:tuple, n:int)->None:
        data_processor = DataPreProcessor('writing_sample')
        common_words = data_processor.get_top_n_grams(corpus=corpus, n_gram_range=n_gram_range, n=n)
        #common_words = self.get_top_n_grams(corpus=corpus, n_gram_range=n_gram_range, n=n)
        df3 = pd.DataFrame(common_words, columns = ['bigram' , 'count'])

        fig = go.Figure([go.Bar(x=df3['bigram'], y=df3['count'])])
        fig.update_layout(title=go.layout.Title(text=f"Top {n} ngrams of length {n_gram_range[0]} in the description text after removing stop words and lemmatization"))
        fig.show()
        
    # def unigram_bar_chart(self, corpus, n):
    #     common_words = self.get_top_n_grams(corpus=corpus, n_gram_range=(1,1), n=n)
    #     df2 = pd.DataFrame(common_words, columns = ['unigram' , 'count'])

    #     fig = go.Figure([go.Bar(x=df2['unigram'], y=df2['count'])])
    #     fig.update_layout(title=go.layout.Title(text=f"Top {n} unigrams in the description text after removing stop words and lemmatization"))
    #     fig.show()

    # def bigram_bar_chart(self, corpus, n):
    #     #common_words = self.get_top_n_bigrams(corpus, n)
    #     common_words = self.get_top_n_grams(corpus=corpus, n_gram_range=(2,2), n=n)
    #     df3 = pd.DataFrame(common_words, columns = ['bigram' , 'count'])

    #     fig = go.Figure([go.Bar(x=df3['bigram'], y=df3['count'])])
    #     fig.update_layout(title=go.layout.Title(text=f"Top {n} bigrams in the description text after removing stop words and lemmatization"))
    #     fig.show()

    # def trigram_bar_chart(self, corpus, n):
    #     #common_words = self.get_top_n_bigrams(corpus, n)
    #     common_words = self.get_top_n_grams(corpus=corpus, n_gram_range=(3,3), n=n)
    #     df3 = pd.DataFrame(common_words, columns = ['bigram' , 'count'])

    #     fig = go.Figure([go.Bar(x=df3['bigram'], y=df3['count'])])
    #     fig.update_layout(title=go.layout.Title(text=f"Top {n} trigrams in the description text after removing stop words and lemmatization"))
    #     fig.show()

    

    