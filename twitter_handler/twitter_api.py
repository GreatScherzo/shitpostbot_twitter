import numpy as np
import pandas as pd
import tweepy
import logging
import csv
import string as st
import os
dir_path = os.getcwd()

class Twitter_Api():
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        self._logger = logging.getLogger(__name__)
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_key = access_key
        self._access_secret = access_secret
        self._authorization = None
        # if consumer_key is None:
        #     self.tweet = lambda x: self._logger.info("Test tweet: " + x)
        #     self._login = lambda x: self._logger.debug("Test Login completed.")

    def _login(self):
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_key, self._access_secret)
        self._authorization = auth

    def tweet(self, tweet):
        if self._authorization is None:
            self._login()
            pass
        api = tweepy.API(self._authorization)
        stat = api.update_status(status=tweet)
        de_tweet = tweet.decode("utf8")
        self._logger.info("Tweeted: " + de_tweet)
        self._logger.info(stat)

    def tweet_media(self, image_path):
        """
        tweet media
        must be filename
        :param shitpost:
        :param image_path:
        :param tweet:
        :return:
        """
        if self._authorization is None:
            self._login()
            pass
        api = tweepy.API(self._authorization)

        absolute_image_path = os.path.join(dir_path, image_path)
        stat = api.update_with_media(filename=absolute_image_path)
        # kata yg atas tu deprecated, tapi yg atas tu ja function
        # api.media_upload(filename=image_path)
        # print("The media ID is : " + stat.media_id_string)
        # print("The size of the file is : " + str(stat.size) + " bytes")

        self._logger.info("Image Tweeted!")
        # this is too much info lol
        # self._logger.info(stat)

    def disconnect(self):
        self._authorization = None


def get_keys(path):
    """
    Parses the key from the given key file path
    :param path:
    :return:
    """
    full_path = os.path.join(dir_path, path)
    content = pd.read_csv(full_path, delimiter=',', header=None)
    Keys = content.values.tolist()

    consumer_key = Keys[0][1]
    consumer_secret = Keys[1][1]
    access_token = Keys[2][1]
    access_secret = Keys[3][1]

    return consumer_key, consumer_secret, access_token, access_secret
