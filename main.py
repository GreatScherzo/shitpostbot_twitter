"""
Entrypoint
"""
import logging

import schedule

from shitpost_api import image_module
import threading
from twitter_handler import twitter_api
import time
import os
from custom_exception import ErrorWithCode
import custom_exception
import random

global_previous_template_num = None
global_previous_insert_img_path = []
global_api_handler = None


class ShitPostWorker():
    """
    TODO: for future expansion
    """

    def __init__(self):
        pass


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def shitpost_time():
    global global_previous_template_num
    global global_previous_insert_img_path
    global global_api_handler

    try:
        logging.info("Started shitpost_time")
        # get template info from template_info.csv
        img_info, current_template_num = image_module.get_random_template_info(global_previous_template_num)
        logging.info("Got random template as below: \n "
                     "{}".format(str(img_info)))

        # parse img_info
        # first create class object for the img template
        img_template_info = image_module.img_info()
        # then parse
        img_template_info.parse_template_info(img_info_dict=img_info)

        # set global previous template num with the curent one for next shitpost post
        global_previous_template_num = current_template_num

        # get template image
        template_img = image_module.get_template_image(img_template_info)

        # get mask for template
        mask = image_module.get_mask_image(img_template_info)

        # threshold mask to remove any noise
        image_module.threshold_image(mask)

        # TODO:check number of insert images needed

        # get random insert image
        insert_img_obj, current_insert_img_path = image_module.get_random_insert_image(img_template_info,
                                                                                       global_previous_insert_img_path)

        logging.info("Got random insert_img as below: \n "
                     "{}".format(str(current_insert_img_path)))

        # set global previous insert img path with the curent one for next shitpost post
        global_previous_insert_img_path = current_insert_img_path

        # place insert image into template image to create shitpost
        image_module.create_shitpost(template_img, mask, insert_img_obj, img_template_info)

        # comment out for debug
        global_api_handler.tweet_media("shitpost.png")
        # ada dah logger interface kat dlm twitter api module
        # logging.info("Posted to twitter")

    except ErrorWithCode as e:
        custom_exception.error_with_code = e
        e.print_exception()
        # logging.info("Error occurred:%s" % str(e.code))
        # exit_code = -1
        pass


def log_in():
    """
    Log in to twitter account
    twitter keys are obtained from the twitter key csv file outside
    :return: api handler
    """
    consumer_key, consumer_secret, access_token, access_secret = twitter_api.get_keys("twitter_key.csv")

    try:
        api_handler = twitter_api.Twitter_Api(consumer_key, consumer_secret, access_token, access_secret)
    except:
        raise Exception("Something went wrong when logging in to twitter account")

    return api_handler


def entrypoint():
    # debug
    # previous_template_num = None
    # api_handler = log_in()
    # previous_template_num = shitpost_time(api_handler, previous_template_num)

    global global_previous_template_num
    global global_previous_insert_img_path
    global global_api_handler

    # set seed so that it wouldn't be based on date
    random.seed("1996")

    # get current working path (Especially needed for Linux)
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # dir_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.getcwd()
    log_file_name = 'log.txt'
    log_file_path = os.path.join(dir_path, log_file_name)

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename=log_file_path,
                        filemode='a+')

    # global_previous_template_num = None
    # global_previous_insert_img_path = []
    # global_api_handler = None

    global_api_handler = log_in()
    shitpost_time()
    schedule.every(2).hours.do(shitpost_time)

    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # debug
    # previous_template_num = None
    # api_handler = log_in()
    # previous_template_num = shitpost_time(api_handler, previous_template_num)

    # get current working path (Especially needed for Linux)
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # dir_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.getcwd()
    log_file_name = 'log.txt'
    log_file_path = os.path.join(dir_path, log_file_name)

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename=log_file_path,
                        filemode='a+')

    global_previous_template_num = None
    global_previous_insert_img_path = []
    global_api_handler = None

    global_api_handler = log_in()
    shitpost_time()
    schedule.every(2).hours.do(shitpost_time)

    while 1:
        schedule.run_pending()
        time.sleep(1)
