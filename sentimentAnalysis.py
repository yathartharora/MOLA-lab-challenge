from transformers import AutoTokenizer,AutoModelForSequenceClassification
from scipy.special import softmax


tweet = "Great content!"

tweet_words = []

for word in tweet.split(' '):
    if word.startswith('@') and len(word)>1:
        word = '@user'
    elif word.startswith('http'):
        word='http'
    tweet_words.append(word)

print(tweet_words)
tweet = " ".join(tweet_words)

modelName = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(modelName)

tokenizer = AutoTokenizer.from_pretrained(modelName)

labels = ['Negative','Neutral','Positive']

encoded_tweet = tokenizer(tweet,return_tensors='pt')
print(encoded_tweet)

# output = model(encoded_tweet['input_ids'],encoded_tweet['attention_mask'])
output = model(**encoded_tweet)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
print(scores)