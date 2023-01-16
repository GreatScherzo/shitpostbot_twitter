
import numpy as np
from nltk.twitter import Twitter
import twython
import tweepy
import json
from pprint import pprint
from tweepy import OAuthHandler

from tweepy import Stream
from tweepy.streaming import StreamListener


import time
import schedule
from datetime import date
import logging

import string as st


class Bot:
    def __init__(self, documents, twitter_api, max_document_length=100, burn_in=25, sleep_time_for_every_tweet=60*60):
        self._documents = documents
        self._twitter_api = twitter_api
        self._corpus = {}
        self._logger = logging.getLogger(__name__)
        self._max_sentence_length = max_document_length
        self._burn_in = burn_in

        # Calculate sleep timer
        self.sleep_timer = int(sleep_time_for_every_tweet)

    def _load_data(self):
        next_key = None
        for doc in self._documents:
            with open(doc, "rb") as f:
                for line in f.readlines():
                    parsed, add = self._line_to_array(line)
                    if add:
                        #kat sini nak selitkan filer boi

                        if next_key is None:
                            a = -2
                        else:
                            a = 0
                        for k in range(0, (len(parsed) + a)):
                            if next_key is not None:
                                key = next_key
                                next_key = (next_key[1], parsed[k])
                            else:
                                key = (parsed[k], parsed[k + 1])

                            self._add_to_corpus(parsed, key, k, next_key)  # You can imagine what this function does
                        if k == len(parsed) - 3 and next_key is None:
                            next_key = (parsed[k + 1], parsed[k + 2])
        self.last_key = next_key

    def _line_to_array(self, line):
        if len(line) < 1:
            return [], False
        line = line.strip()
        line = line.split()

        #buang kat sini, pakai regex
        return line, True

    def _add_to_corpus(self, parsed, key, k, next_key):
        if next_key is None:
            addition = 2
        else:
            addition = 0

        word = parsed[k + addition]

        if key in self._corpus:
            self._corpus[key].append(word)
        else:
            self._corpus[key] = [word]

    def _generate_text(self, size=10000):
        size += self._burn_in  # For a burn in of 250 words.
        start_word = self._grab_random_two_words()
        text = [''] * size
        cap = [False] * size
        cap[0] = True
        text[0] = start_word[0]
        text[1] = start_word[1]

        punc = set(st.punctuation)

        # Create Sample
        i = 2
        while i < size:
            if any([True if k in punc and k != ',' else False for k in text[i - 1]]):
                cap[i] = True
            key = (text[i - 2], text[i - 1])
            if key == self.last_key:
                # Restart if last key is chosen
                new_key = self._grab_random_two_words()
                text[i] = new_key[0]
                if i + 1 < size:
                    text[i + 1] = new_key[1]
                key = new_key
                i += 2
            choice = np.random.choice(self._corpus[key])
            if i < size:
                text[i] = choice
            i += 1

        # Capitalize
        for k in range(0, size):
            if cap[k]:
                text[k] = text[k].capitalize()
            if k == size - 1:
                if not any([True if j in punc and j != '\'' else False for j in text[k]]):
                    text[k] = text[k] + b'.'
        # Find the first period after the burn in section
        for first_period in range(self._burn_in, size):
            if b'.' in text[first_period]:
                break
        return b' '.join(text[(first_period + 1):]).strip()


    def _get_tweet(self):
        tweet = ''
        while tweet == '':
            num_words = np.random.randint(2, self._max_sentence_length)
            temp = self._generate_text(num_words).split(b".")
            k = 0
            for k in range(0, len(temp)):
                if len(temp[k]) > 20:
                    break
            for i in range(len(temp), -1, -1):
                pos_tweet = b'.'.join(temp[k:(i + 1)])
                if len(pos_tweet) < 140 and len(temp) > 20:  # 140 due to adding a period
                    tweet = pos_tweet + b"."
                    break
        return tweet.strip().replace(b"\"", b"")



    def _grab_random_two_words(self):
        start = np.random.randint(0, len(self._corpus))
        start_word = list(self._corpus.keys())[start]
        return start_word




    def run(self):
        self._load_data()  # Here it loads the corpora and converts them into a transition matrix
        while True:
            try:
                tweet = self._get_tweet()  # Samples
                self._twitter_api.tweet(tweet)  # Posts to twitter
            except Exception as e:
                self._logger.error(e, exc_info=True)
                self._twitter_api.disconnect()
            time.sleep(self.sleep_timer)  # Every 10 minutes
            #TODO: make that https arent sampled
