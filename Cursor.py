#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing

import matplotlib.pyplot as plt #For Visualization


# In[2]:


# Consume:
CONSUMER_KEY    = 'o3Tp9FOv1NwexvJp2nhk3Nktk'
CONSUMER_SECRET = 'RlMysPpdhwU7EChDTdI2r6PkS9VpP1g0npJWAFS4pw3y8Qxje0'

# Access:
ACCESS_TOKEN  = '353552130-vQA2Wl4cnzCL17rzdr4GF00EWwQsFYWP4S2RMz8n'
ACCESS_SECRET = 'gdk4zrHNMeXDFGnH9ljrixcOGETqWc2FAsBKxTOFoVvvD'


# In[3]:


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


# In[4]:


extractor = twitter_setup()
msgs = []
msg =[]

#Extracts tweet based on Hashtags:
try:
    for tweet in tweepy.Cursor(extractor.search, q='flipkart', rpp=100).items(2000):
        msg = [tweet.text, tweet.source,len(tweet.text),tweet.id,tweet.created_at,tweet.favorite_count,tweet.source_url] 
        msg = tuple(msg)                    
        msgs.append(msg)
        data = pd.DataFrame(msgs,columns=['tweets', 'source','len','ID','Date','Likes','url'])
except Exception as ex:
    print(ex)


# In[5]:


data.head(10)


# In[7]:


#Counts the number tweets fetched column wise
data.count()


# In[8]:


from textblob import TextBlob
import re

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


# In[9]:


data['sentimnt_analys'] = np.array([ analize_sentiment(tweet) for tweet in data['tweets'] ])

# We display the updated dataframe with the new column:
display(data.head(10))


# In[10]:


#Tweet Segregation:

pos_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['sentimnt_analys'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['sentimnt_analys'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['sentimnt_analys'][index] < 0]


# In[11]:


# We print percentages:

print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['tweets'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['tweets'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['tweets'])))


# In[12]:


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Positive', 'Neutral', 'Negative'
sizes = [len(pos_tweets)*100/len(data['tweets']),len(neu_tweets)*100/len(data['tweets']),len(neg_tweets)*100/len(data['tweets'])]
explode = (0.1, 0, 0)  # only "explode" the 2nd slice
color=['green','yellow','red']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90, colors=color)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

