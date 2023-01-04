import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector
from flask import Flask, request, jsonify


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


app = Flask(__name__)

@app.route('/api/language-detection',methods=['POST'])
def detection():
    languageDetection = []
    input = request.get_json(force=True)
    for item in input:
        languageDetection.append({"tweet_text":item["tweet_text"],"is_english": returnBool(item["tweet_text"])})
    return jsonify(languageDetection)

if __name__ == '__main__':
    app.run(debug=True)