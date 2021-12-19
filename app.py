
import tweepy
import pandas as pd
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
from flask import Flask, request, render_template, session, redirect
import time

CLOUD_FOLDER = os.path.join('static', 'img')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = CLOUD_FOLDER

#app.secret_key = "manbearpig_MUDMAN888"

consumer_key = "czjmPINpFQj6KeS06Aelyu7IV" 
consumer_secret = "And7NNiRSmTWBPGoWQ7P67Bs90SKCTJcdSo29RiYrabVrKSdov"
access_token = "390017143-aFAyz2FmIvzWPe7GEGBR8H9DyO2kmW8qrxHhBTUP"
access_token_secret = "MU7XDR7D8HPgsmodLsc4qISAJlSFJwmofXR8AD2ba3dRw"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def reading_tweets(keyword,recent):
  try:
    tweets = tweepy.Cursor(api.search_tweets,q=keyword,lang='en').items(recent) #creates query method
    tweets_list = [[tweet.text] for tweet in tweets]
    #pulls text information from tweets
    df = pd.DataFrame(tweets_list,columns=['Text'])
    print("Cleaning the tweets...\n")
    cleaned_tweets = []
    for i in range(0,df.shape[0]):
      cleaned_tweets.append(cleaning_tweets((df.Text[i])))
    string = pd.Series(cleaned_tweets).str.cat(sep=' ')
    wordcloud(string)
    return df
    #creates a csv from data frame
  except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)


def cleaning_tweets(t):
    re.compile('<title>(.*)</title>');
    re_list = ['@[A-Za-z0–9_]+', '#']
    combined_re = re.compile( '|'.join( re_list))
    regex_pattern = re.compile(pattern = "["
       u"\U0001F600-\U0001F64F"  # emoticons
       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
       u"\U0001F680-\U0001F6FF"  # transport & map symbols
       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          "]+", flags = re.UNICODE)
    token = WordPunctTokenizer()
    del_amp = BeautifulSoup(t, 'lxml')
    del_amp_text = del_amp.get_text()
    del_link_mentions = re.sub(combined_re, '', del_amp_text)
    del_emoticons = re.sub(regex_pattern, '', del_link_mentions)
    lower_case = del_emoticons.lower()
    words = token.tokenize(lower_case)
    result_words = [x for x in words if len(x) > 2]
    return (" ".join(result_words)).strip()

def wordcloud(string):
    stopwords = set(STOPWORDS)
    stopwords.update(["https"])
    wordcloud = WordCloud(width=1600, stopwords=stopwords,height=800,max_font_size=200,max_words=60,collocations=False, background_color='black').generate(string)
    plt.figure(figsize=(40,30))
   #plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
   # plt.show()
    wordcloud.to_file(os.path.join(app.config['UPLOAD_FOLDER'], 'cloud.png'))
    

@app.route("/")
def html():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'cloud2.png')
    return render_template("index.html", image= full_filename)

@app.route('/submit', methods =['POST', 'GET'])
def submit():
    if request.method == 'POST':
        hashtag = request.form['hashtag'] + " -filter:retweets"
        tweets = request.form['tweets']
        reading_tweets(str(hashtag), int(tweets))
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'cloud.png')
    return render_template("index.html", image= full_filename)

if __name__ == '__main__':
    app.run(debug=True)