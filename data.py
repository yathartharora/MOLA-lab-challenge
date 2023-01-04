import requests

data = [
 {
   "tweet_text": "Stats on Twitter World Cup"
 },
 {
   "tweet_text": "As the saying goes, be careful what you wish, as you might get it"
 },
 {
   "tweet_text": "شب یلدا مبارک! ❤️"
 }
]


res = requests.post("http://127.0.0.1:5000/api/language-detection",json=data)
print(res.text)