import tweepy
from tweepy import OAuthHandler

import time
import schedule
import logging
import threading

from twitter_handler import QuoteBot, twitter_api, TweetGrabber

# from importlib.machinery import SourceFileLoader
# SourceFileLoader("STD", r"C:\Users\Barzarin\OneDrive\jupyter\speech_to_data.py").load_module()
# SourceFileLoader("STD", r"C:\Users\Barzarin\OneDrive\jupyter\speech_to_data.py").load_module()


consumer_key = '3qgkrUwgoyijjqkWDQQI7S07W'
consumer_secret = '1DEnFmKaiGEDGCfljs8p4B6UaQMcfRXcz3Txxc5kwzOyPH6wJ0'
access_token = '1037339572705755138-yKP5WKZOuF12NwHuz1CktfOekvINwl'
access_secret = 'FvUZlJAVKvn0pyS1GACUvH94mIjrkAKRZDT4ePku3K3JW'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api2 = tweepy.API(auth)

name1 = "TheStoicEmperor"
name2 = "InspowerBooks"
name3 = "ItsLifeFact"
name4 = "wordstionary"
name5 = "FactSoup"


def main():
    # Configure Logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


    documents = ["res/name1.txt",
                 "res/name2.txt",
                 "res/name3.txt",
                 "res/name4.txt",
                 "res/name5.txt"]  # Specify the documents

    twitter_api = twitter_api.Twitter_Api(consumer_key, consumer_secret, access_token, access_secret)
    bot = QuoteBot.Bot(documents, twitter_api)

    bot.run()

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


# _name_ ialah special variable, dan bila name equals to main, maksudnya module(program) ni main program ah
if __name__ == "__main__":

    #debug
    #schedule.every().seconds.do(run_threaded, main())#masa dia tulis kat bot
    #schedule.every(2).seconds.do(run_threaded,TweetGrabber.grab_tweets(1))

    schedule.every().hours.do(run_threaded, main())  # masa dia tulis kat bot
    schedule.every(2).hours.do(run_threaded, TweetGrabber.grab_tweets(1))

    
    while 1:
        schedule.run_pending()
        time.sleep(1)


    # grabThread = threading.Thread(target=TweetGrabber.run_grabber())
    # botThread = threading.Thread(target=main())
    #
    # threads = list()
    # threads.append(botThread)
    # threads.append(grabThread)
    #
    #
    # for index in range(2):
    #     threads[index].start()
