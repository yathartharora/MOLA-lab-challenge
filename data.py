import requests

data = [
 {
   "tweet_text": "Great Content!"
 },
 {
   "tweet_text": "This is not how it is done! Very Bad"
 }
]


res = requests.post("http://127.0.0.1:5000/api/sentiment-score",json=data)
print(res.text)