# In[2]:


import tweepy
from tweepy import OAuthHandler

from twitter_handler import Main


# In[8]:


#TODO: terus di detect berapa byk sources yg ada dari Main, lps tu process ikut bilangan sources tu ja

def grab_tweets(tweetCount):
    # Calling the user_timeline function with our parameters
    results1 = api2.user_timeline(id=name1, count=tweetCount)
    results2 = api2.user_timeline(id=name2, count=tweetCount)
    results3 = api2.user_timeline(id=name3, count=tweetCount)
    results4 = api2.user_timeline(id=name4, count=tweetCount)
    results5 = api2.user_timeline(id=name5, count=tweetCount)

    # foreach through all tweets pulled
    for tweet in results1:
        # printing the text stored inside the tweet object
        with open("../res/name1.txt", 'w') as f:
            f.write(tweet.text.encode("utf-8"))

    for tweet in results2:
        # printing the text stored inside the tweet object
        with open("../res/name2.txt", 'w') as f:
            f.write(tweet.text.encode("utf-8"))

    for tweet in results3:
        # printing the text stored inside the tweet object
        with open("../res/name3.txt", 'w') as f:
            f.write(tweet.text.encode("utf-8"))

    for tweet in results4:
        # printing the text stored inside the tweet object
        with open("../res/name4.txt", 'w') as f:
            f.write(tweet.text.encode("utf-8"))

    for tweet in results5:
        # printing the text stored inside the tweet object
        with open("../res/name5.txt", 'w') as f:
            f.write(tweet.text.encode("utf-8"))

        # In[9]:


auth = OAuthHandler(Main.consumer_key, Main.consumer_secret)
auth.set_access_token(Main.access_token, Main.access_secret)
api2 = tweepy.API(auth)

name1 = Main.name1
name2 = Main.name2
name3 = Main.name3
name4 = Main.name4
name5 = Main.name5

# In[7]:

#Old Scheduling
# schedule.every().day.at("10:30").do(grab_tweets, 1000)
# schedule.every().day.at("20:30").do(grab_tweets, 1000)

# def run_grabber():
#     #debugging
#     schedule.every(2).seconds.do(grab_tweets, 1000)
#
#     #real
#     #schedule.every(2).hours.do(grab_tweets, 1000)
#
#     while True:
#         run_grabber()
#         schedule.run_pending()
#         time.sleep(1)

