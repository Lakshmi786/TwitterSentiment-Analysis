#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import flask
from flask import Flask, render_template, request
import pickle

# Running the flask app
app = Flask(__name__)

#load model using pickle
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
def text_preprocessing(s):
    import re
    import nltk
# Uncomment to download "stopwords"
    nltk.download("stopwords")
    from nltk.corpus import stopwords
    """
    - Lowercase the sentence
    - Change "'t" to "not"
    - Remove "@name"
    - Isolate and remove punctuations except "?"
    - Remove other special characters
    - Remove stop words except "not" and "can"
    - Remove trailing whitespace
    """
    s = s.lower()
    # Change 't to 'not'
    s = re.sub(r"\'t", " not", s)
    # Remove @name
    s = re.sub(r'(@.*?)[\s]', ' ', s)
    # Isolate and remove punctuations except '?'
    s = re.sub(r'([\'\"\.\(\)\!\?\\\/\,])', r' \1 ', s)
    s = re.sub(r'[^\w\s\?]', ' ', s)
    # Remove some special characters
    #s = re.sub(r'([\;\:\|•«\n])', ' ', )
    s = re.sub('[^A-Za-z0-9]+', ' ', s)
    # Remove stopwords except 'not' and 'can'
    s = " ".join([word for word in s.split()
                  if word not in stopwords.words('english')
                  or word in ['not', 'can']])
    # Remove trailing whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    
    return s

@app.route('/', methods=['POST'])
def predict():
    feature = str([str(x) for x in request.form.values()])
    int_feature = text_preprocessing(feature)
    print('int_feature',int_feature)
    prediction = model.predict([int_feature])
    if prediction == 0:
        senti = 'Positive'
    else:
        senti = 'Negative'

    return render_template('index.html', prediction_text='The sentiment of tweet is {}'.format(senti))

if __name__ == '__main__':
    app.run(debug=True)

