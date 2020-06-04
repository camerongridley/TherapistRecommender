from flask import Flask, render_template, request, jsonify
import pickle
from build_model import TextClassifier

app = Flask(__name__)

model = pickle.load( open( "../deploy/nmf_model", "rb" ) )
vectorizer = pickle.load( open( '../deploy/nmf_vectorizer', "rb" ) )
df_therapist_topics = pickle.load( open( '../deploy/nmf_df_topics', "rb" ) )

with open('../delpoy/nmf_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET'])
def submit():
    return render_template('submit.html')

@app.route('/recommend', methods=['POST'])
def recommend():

    content = str(request.form['writing_sample'])
    pred = model.predict([content])[0]

    return render_template('recommend.html', article=content, predicted=pred)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
