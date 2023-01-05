import string
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector
from flask import Flask, request, jsonify
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax
from flask_cors import CORS, cross_origin



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
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/language-detection',methods=['POST'])
@cross_origin()
def detection():
    languageDetection = []
    input = request.get_json(force=True)
    for item in input:
        languageDetection.append({"tweet_text":item["tweet_text"],"is_english": returnBool(item["tweet_text"])})
    return jsonify(languageDetection)

@app.route('/api/sentiment-score',methods=['POST'])
@cross_origin()
def sentiment():
    modelName = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    labels = ['Negative','Neutral','Positive']
    sentimentDetection = []
    input = request.get_json(force=True)
    for item in  input:
        tweet = filterWord(item["tweet_text"])
        encoded_tweet = tokenizer(tweet,return_tensors='pt')
        output = model(**encoded_tweet)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        # print(scores)

        if scores[0] > scores[1] and scores[0] > scores[2]:
            detected = "NEGATIVE"
        elif scores[1] > scores[0] and scores[1] > scores[2]:
            detected = "NEUTRAL"
        else:
            detected = "POSITIVE"

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
    app.run(debug=True)