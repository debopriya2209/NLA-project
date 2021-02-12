#!/usr/bin/env python
# coding: utf-8

# In[24]:


import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np       # For number computing
from textblob import TextBlob
import re

#import matplotlib.pyplot as plt #For Visualization

# Consume:
CONSUMER_KEY    = 'o3Tp9FOv1NwexvJp2nhk3Nktk'
CONSUMER_SECRET = 'RlMysPpdhwU7EChDTdI2r6PkS9VpP1g0npJWAFS4pw3y8Qxje0'

# Access:
ACCESS_TOKEN  = '353552130-vQA2Wl4cnzCL17rzdr4GF00EWwQsFYWP4S2RMz8n'
ACCESS_SECRET = 'gdk4zrHNMeXDFGnH9ljrixcOGETqWc2FAsBKxTOFoVvvD'


def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

def fetch_tweet(word):
    extractor = twitter_setup()
    msgs = []
    msg =[]

    #Extracts tweet based on Hashtags:
    try:
        for tweet in tweepy.Cursor(extractor.search, q=word, rpp=100).items(2000):
            msg = [tweet.text, tweet.source,len(tweet.text),tweet.id,tweet.created_at,tweet.favorite_count,tweet.source_url] 
            msg = tuple(msg)                    
            msgs.append(msg)
            data = pd.DataFrame(msgs,columns=['tweets', 'source','len','ID','Date','Likes','url'])
        print("dataSize->",data.count())
        return data
    except Exception as ex:
        print(ex)
        return ex



def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
#     print(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

def sentiment_percentage(word):
    
    data=fetch_tweet(word)
    
    data['sentimnt_analys'] = np.array([ analize_sentiment(tweet) for tweet in data['tweets'] ])
    
    pos_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['sentimnt_analys'][index] > 0]
    neu_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['sentimnt_analys'][index] == 0]
    neg_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['sentimnt_analys'][index] < 0]
    
    percent_pos_tweets=(len(pos_tweets)*100/len(data['tweets']))
    percent_neu_tweets=(len(neu_tweets)*100/len(data['tweets']))
    percent_neg_tweets=(len(neg_tweets)*100/len(data['tweets']))
    
    top_five=data['tweets'].head(5)
    top_three_pos_tweets=pos_tweets[0:3]
    top_three_neu_tweets=neu_tweets[0:3]
    top_three_neg_tweets=neg_tweets[0:3]
 
    
    return top_five,percent_pos_tweets,percent_neu_tweets,percent_neg_tweets,top_three_pos_tweets,top_three_neu_tweets,top_three_neg_tweets









