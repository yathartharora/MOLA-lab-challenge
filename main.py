import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def isEnglish(nlp,name):
    return LanguageDetector(seed=42)


model = spacy.load("en_core_web_sm")

Language.factory("language_detector",func=isEnglish)
model.add_pipe('language_detector',last=True)


def returnBool(tweet):
    doc = model(tweet)
    language = doc._.language
    if language['language'] == 'en' and language['score']>=0.8:
        return True
    else:
        return False

def filterWord(tweet):
    tweet_words = []
    for word in tweet.split(' '):
        if word.startswith('@') and len(word)>1:
            word = '@user'
        elif word.startswith('http'):
            word='http'
        tweet_words.append(word)
    return " ".join(tweet_words)


app = Flask(__name__)
cors = CORS(app,resources={r"/api/*": {"origins": "https://twitter.com"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/language-detection',methods=['POST'])
@cross_origin(origins="*",supports_credentials=True)
def detection():
    languageDetection = []
    input = request.get_json(force=True)
    for item in input:
        languageDetection.append({"tweet_text":item["tweet_text"],"is_english": returnBool(item["tweet_text"])})
    return jsonify(languageDetection)


@app.route('/api/sentiment-score',methods=['POST'])
@cross_origin(origins="*",headers=['Content- Type'])
def sentiment():
    # elif request.method == "POST":
    labels = ['Negative','Neutral','Positive']
    sentimentDetection = []
    input = request.get_json(force=True)
    # print(input)
    for item in input:
        scores = [0] * 3
        tweet = filterWord(item["tweet_text"])
        data = {"text": tweet}
        res = requests.post(API_URL,headers=headers,json=data)
        # print(res.status_code)
        if res.status_code==200:
            detected = res.json()[0]['label'].upper()
            for labels in res.json():
                if labels['label'] == 'positive':
                    scores[2] = labels['score']
                elif labels['label'] == 'neutral':
                    scores[1] = labels['score']
                else:
                    scores[0] = labels['score']

            sentimentDetection.append({
                    "tweet_text": item["tweet_text"],
                    "sentiment_score": {
                    "positive": float(scores[2]),
                    "neutral": float(scores[1]),
                    "negative": float(scores[0])
                },
                "detected_mood": detected
            })
    return jsonify(sentimentDetection)
        



if __name__ == '__main__':
    app.run(debug=True,threaded=False)