"""
Module that handles the image cropping and shit
when making the shitpost

"""
import os
from typing import Union, List

import pandas as pd
import random
from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
from custom_exception import ErrorWithCode

# the problem with getcwd, is that it gets the path of the current file being executed
# if, lets say, you run a software and that software calls this python program, then
# the path that getcwd gets is the software you ran
# which would result in the python program to not run properly

# ok, os path dirname abspath also has its problem. It does get the python program's path, but
# if that is done in a python module (which its directory is different from main python file),
# it will get the module's path

dir_path = os.getcwd()
# dir_path = os.path.dirname(os.path.abspath(__file__))

class img_info():
    def __init__(self):
        self.chosen_template_name = None
        self.must_use_label = None
        self.labels = None
        self.num_of_inserts = None
        self.enable_alpha_insert = None

    def parse_template_info(self, img_info_dict: dict):
        self.chosen_template_name = img_info_dict['name']
        self.must_use_label = img_info_dict['must_use_label']

        self.labels = img_info_dict['label']
        if type(self.labels) == str:
            self.labels = str.split(self.labels, ',')
        elif type(self.labels) == float:
            self.labels = None

        self.num_of_inserts = img_info_dict['num_of_inserts']
        self.enable_alpha_insert = img_info_dict['enable_alpha_insert']


def get_template_info():
    """
    Gets info of the template image. The info are as below

    Template Info
    ============
    id
        id of the image

    alpha_area_shape
        shape of alpha region to insert image

    alpha_box_position
        top left postion and top right position of area to be insert with a
        For shape of circle, radius and centre of circle in used

    labels
        labels of

    absurdness
        the level of absurness as to calculate level of relevance




    :return:
    """


def get_random_template_info(previous_template_num: Union[int, None]):
    """
    to initiate the bot, the bot will first
    need a random template image to be used

    python's random module uses current data and time as seed
    :return: Info of selected template image
    """

    # Get template image data
    # path_template_info = r".\res\image\template_info.csv"
    path_template_info = os.path.join(dir_path, 'res', 'image', "template_info.csv")
    # id_all = pd.read_csv(path_template_info, delimiter=",", usecols=['id'])
    template_data = pd.read_csv(path_template_info, delimiter=",")

    # Get length of data
    len_of_template_data = len(template_data)

    # Select random template data
    possible_template_nums = range(len_of_template_data)
    selected_id = random.choice(possible_template_nums)
    # if it is the same template as before,
    # continue retrying until a different one is chosen
    if previous_template_num != None:
        while selected_id == previous_template_num:
            selected_id = random.choice(possible_template_nums)

    # get the selected template data
    selected_info = template_data.iloc[selected_id]

    return selected_info.to_dict(), selected_id


def get_template_image(img_template_info: img_info):
    """
    gets template image based on name
    :return:
    """
    # get template name
    template_name = img_template_info.chosen_template_name

    # img_path = os.path.join(".\\res\\image\\template_image", (image_name + ".jpg"))
    img_path = os.path.join(dir_path, 'res', 'image', 'template_image', (template_name + ".jpg"))
    im = Image.open(img_path)
    return im


def get_mask_image(img_template_info: img_info):
    """
    gets mask image
    :return:
    """
    # get template name
    template_name = img_template_info.chosen_template_name

    # concatenate _mask with the name to get mask
    # img_path = os.path.join(".\\res\\image\\mask", (image_name + "_mask" + ".bmp"))
    img_path = os.path.join(dir_path, 'res', 'image', "mask", (template_name + "_mask" + ".bmp"))
    img = cv2.imread(img_path, 0)

    # Open image as 8-bit grayscale
    # im = Image.open(img_path).convert('L')
    return img


def get_random_insert_image(img_template_info: img_info, previous_insert_img_path):
    """
    gets insert image to create shitpost
    TODO: in future, weighted choice would be used based on label
    :return:
    """

    def _get_related_paths(template_info: img_info):
        """
        Get the related paths if img labels is required
        Otherwise, return all image paths available
        :param template_info:
        :return:
        """
        # TODO: get num of images to be picked

        # if labels are needed, get every images in the specified labels
        _img_folder_to_be_picked = []
        _all_img = []  # all img path to choose from
        if template_info.must_use_label:
            # search for the folder specified by the template's label
            for root, dirs, files in os.walk(img_path):
                for name in dirs:
                    if name in template_info.labels:
                        # append those folder to imgfoldertobepicked
                        _img_folder_to_be_picked.append(os.path.join(root, name))

            # Now that the paths for the labels folder is acquired, get each images path in the folder
            for current_path in _img_folder_to_be_picked:
                # get all images path
                all_img_name = os.listdir(current_path)
                # map it with the root to make it abs
                abs_all_img_name = list(map(lambda x: os.path.join(current_path, x), all_img_name))
                # extend it to all img array
                _all_img.extend(abs_all_img_name)

        # if labels are not needed, straight up get all paths of each image in database
        else:
            # _all_img = os.listdir(img_path)
            # below is a double for each style loop
            _all_img = [os.path.join(root, single_file) for root, dirs, files in os.walk(img_path)
                        for single_file in files]

            # dia amek folder name shj, betulkan supaya dia amek path gambar

        return _all_img

    # ###############################################################################################

    # get root folder
    img_path = os.path.join(dir_path, 'res', 'image', "insert_image")

    # get the paths related
    all_img = _get_related_paths(img_template_info)

    # randomly choose an image
    # make sure it isn't the same as the previous insert img
    true_selected_img = []
    # a really complicated filter is made to get random image, so bear with me here
    # randomly choose image and put it in temporary list
    _selected_img = random.sample(all_img, img_template_info.num_of_inserts)
    # gotta clone the choice array, because after removing it, it interferes with the foreach iteration below
    clone_selected_img = _selected_img.copy()
    for single_selected_img in _selected_img:
        # remove the current img selected so that the list can be used as a condition
        # the randomly chosen img must not be the same as the other chosen images
        clone_selected_img.remove(single_selected_img)

        # as long as the image satisfy the conditions below, random sampling will
        # be repeated until a unique image is chosen
        while single_selected_img in previous_insert_img_path or \
                single_selected_img in clone_selected_img or \
                single_selected_img in true_selected_img:
            single_selected_img = random.sample(all_img, 1)

        # append the cleanly filtered image choice, but it will still be used the next iteration
        true_selected_img.append(single_selected_img)

    # while true_selected_img == previous_insert_img_path:
    #     true_selected_img = random.choice(all_img)

    # Open image as 8-bit grayscale
    im_obj = []
    # im = list(map(lambda x: os.path.join(img_path, x), true_selected_img))
    for current_im in true_selected_img:
        im_obj.append(Image.open(current_im))

    # im = Image.open(os.path.join(img_path, true_selected_img))

    return im_obj, true_selected_img


def create_shitpost(template_image: Image.Image, mask, insert_image: List[Image.Image], img_template_info: img_info):
    """
    paste insert image to
    :param img_template_info:
    :param insert_image:
    :param template_image:
    :param mask:
    :return:
    """
    # get connected components
    output = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    # after getting the output from the opencv function, some processing needed to be done so that the data
    # from the output can be understand
    # also, small noises are filtered from here
    (numLabels, labels, stats, centroids) = output
    filtered_labels, x_coor, y_coor, width, height, area = _loop_stats(numLabels, stats, centroids)

    # filter the first one, which is the background (black one in mask)
    filtered_labels.pop(0)
    x_coor.pop(0)
    y_coor.pop(0)
    width.pop(0)
    height.pop(0)
    area.pop(0)

    # num_of_labels_available = len(filtered_labels) - 1
    # get the amount of true labels in the image by subtracting with 1 (excluding the background label)

    num_of_label_spaces_available = len(filtered_labels)

    num_of_img_to_be_insert = len(insert_image)
    """
    at create shitpost, the flag num_of_inserts is not used, because it is used
    in get_random_insert_img, so the resulting insert_img list will have the correct amount
    
    however, an assert will be done to check if the insert_img amount is correct
    """
    # raise ErrorWithCode("0001")

    if (num_of_img_to_be_insert == 1 or num_of_img_to_be_insert == num_of_label_spaces_available):
        pass
    else:
        raise ErrorWithCode("0001")

    j = None

    # in the new update, all output image is made to handle alpha channel
    template_image = template_image.convert('RGBA')

    for i in range(0, num_of_label_spaces_available):
        if num_of_img_to_be_insert > 1:
            j = i
        elif num_of_img_to_be_insert == 1:
            j = 0

        # gets the last label (which apparently is always white coloured luckily)
        componentMask = (labels == filtered_labels[j]).astype("uint8") * 255

        # get the last y coor and stuff and cut it off from the label
        cropped_part = componentMask[y_coor[j]:(y_coor[j] + height[j]), x_coor[j]:(x_coor[j] + width[j])]

        # create temp mask
        true_mask = Image.fromarray(cropped_part)

        # Just as anakin said, this is where the fun part begins
        # resize image based on the temp mask
        temp_insert_image = insert_image[j].resize(true_mask.size)

        # if enable alpha insert, add transparency to insert image
        # this crops the image, by making black areas transparent
        temp_insert_image.putalpha(true_mask)

        if img_template_info.enable_alpha_insert:
            # add alpha value to all white pixels in mask
            temp_mat = temp_insert_image.getdata()

            set_alpha = 128
            new_data = []
            for item in temp_mat:
                if item[3] == 0:
                    # add 100 to alpha channel (making it transparent)
                    # 0:transparent, 255: oblique
                    new_data.append((item[0], item[1], item[2], item[3]))
                else:
                    new_data.append((item[0], item[1], item[2], set_alpha))
            # update true mask to new image
            temp_insert_image.putdata(new_data)

            # for item in temp_mat:
            #     if item[0] == 255 and item[1] == 255 and item[2] == 255:
            #         # add 100 to alpha channel (making it transparent)
            #         # 0:transparent, 255: oblique
            #         new_data.append((255, 255, 255, 100))
            #     else:
            #         new_data.append(item)
            # update true mask to new image
            # true_mask.putdata(new_data)
            #
            # temp_insert_image.putalpha(true_mask)

        # insert the image based pm the labels coordinates
        template_image.alpha_composite(temp_insert_image, (x_coor[j], y_coor[j]))
        # template_image.paste(temp_insert_image, (x_coor[j], y_coor[j]), mask=true_mask)

    # create temp shitpost jpg
    template_image.save(os.path.join(dir_path, "shitpost.png"))

    return None


def _loop_stats(numLabels, stats, centroids):
    # variables
    height_limit = 10  # [pix]
    width_limit = 10  # [pix]
    # loop over the number of unique connected component labels
    filtered_labels, x, y, w, h, area = [], [], [], [], [], []

    for i in range(0, numLabels):
        # if this is the first component then we examine the
        # *background* (typically we would just ignore this
        # component in our loop)
        if i == 0:
            text = "examining component {}/{} (background)".format(
                i + 1, numLabels)
        # otherwise, we are examining an actual connected component
        else:
            text = "examining component {}/{}".format(i + 1, numLabels)
        # print a status message update for the current connected
        # component
        print("[INFO] {}".format(text))
        # extract the connected component statistics and centroid for
        # the current label

        # Filter the noises that occur
        if stats[i, cv2.CC_STAT_WIDTH] >= height_limit and stats[i, cv2.CC_STAT_HEIGHT] > width_limit:
            filtered_labels.append(i)
            x.append(stats[i, cv2.CC_STAT_LEFT])
            y.append(stats[i, cv2.CC_STAT_TOP])
            w.append(stats[i, cv2.CC_STAT_WIDTH])
            h.append(stats[i, cv2.CC_STAT_HEIGHT])
            area.append(stats[i, cv2.CC_STAT_AREA])
            (cX, cY) = centroids[i]

        # starting_coordinates = [x, y]
        # size_of_insert_area = [w, h]

    return filtered_labels, x, y, w, h, area
    # return starting_coordinates, size_of_insert_area, area_of_label

    # TODO: extension for image with more than one insertion image


def get_background_image():
    pass


def calculate_relevance():
    pass


def store_template():
    pass


def store_insert_imamge():
    pass


def threshold_image(img):
    """
    Binarize the image, it doesnt need any return
    :param img:
    :return:
    """
    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)

    return None
