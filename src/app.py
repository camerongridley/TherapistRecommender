from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import numpy as np
from nmf_recommender import NmfRecommender

app = Flask(__name__)

text_col = 'writing_sample'
nmf_recommender = NmfRecommender(text_col)
model = pickle.load( open( "../deploy/nmf_model.pkl", "rb" ) )
vectorizer = pickle.load( open( '../deploy/nmf_vectorizer.pkl', "rb" ) )
df_therapist_topics = pickle.load( open( '../deploy/nmf_df_topics.pkl', "rb" ) )

df_alt_names = pd.read_csv('../deploy/forbes_celebrity_100.csv')


all_states = df_therapist_topics['state'].unique()
all_states.sort()

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html', current_page='INDEX')

@app.route('/submit', methods=['GET'])
def submit():
    return render_template('submit.html', current_page='SUBMIT', state_list=all_states)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html' ,current_page='ABOUT')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', current_page='CONTACT')

@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html', current_page='CONTACT')

@app.route('/recommend', methods=['POST'])
def recommend():
    #np.random.seed(10)
    
    content = str(request.form[text_col])
    print(f'content: {content}')

    if content.strip() == "":
        return render_template('submit.html', current_page='SUBMIT', state_list=all_states, msg='Please tell us about what you are looking for help with.')

    if len(content.strip()) < 200:
        return render_template('submit.html', current_page='SUBMIT', state_list=all_states, msg='We need to know more about you before being able to make good recommedations. Please use at least 200 words.')

    print(df_therapist_topics.head())
    
    n_recs = int(request.form['num_recs_choice'])
    state = str(request.form['state'])

    test = '''
    Although I have been healing for the past two years with lot of therapy and self care . 
    I don’t feel “normal” . I am not the same person as I was when I was 18 . It is frustrating and 
    sometimes causes me to unable to do things I really want to do . For example , I want to date people 
    and experience more sex but I can’t bring myself to do it . Every time I have feelings for someone , 
    I ended up telling myself that I don’t deserve to be with that person because for years , I have 
    convinced myself that I am “broken “ . I feel that a lot of my experiences to explore more of my 
    sexuality and sex was robbed by an event I had when I was eighteen . I ran away from it 
    by joining a Christian campus group which I regret deeply . I was even more further shamed for my 
    sexuality and a desire to have sex . Thankfully , I left that group ,later joined a university 
    in a diverse city after I graduated from a community college . I am super happy that I did because 
    I finally was able to learn what an healthy sex life looks like . I had feelings for several people 
    but was unable to tell them . I even joined tinder and met some people but I freaked out and stop 
    responding to people that I was interested in dating ( I know it is a dick move, I was paralyzed 
    with fear . I still feel guilty about it ) . I want to stop being paranoid about people but honestly 
    it really because I don’t trust myself sometimes . I hate it . I hate that it made me feel 
    invalidated. I have this stupid fear that people wouldn’t want to be with me because I haven’t have 
    a lot of experience in having sex. I am 27 now and I haven’t been in relationships or have sex or 
    dated . What is wrong with me ?
    '''

    loadings, recs = nmf_recommender.classify_and_recommend(model, vectorizer, content,df_therapist_topics, state, n_recs)
    dom_topic_names = '  |  '.join(nmf_recommender.get_dominant_topics(3, loadings)).rstrip()
    #pred = nmf_recommender.predict([content])[0]

    return render_template('recommend.html', current_page='RECOMMEND', topics=dom_topic_names, recommendations=recs, alt_names=df_alt_names)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8105, debug=True)
