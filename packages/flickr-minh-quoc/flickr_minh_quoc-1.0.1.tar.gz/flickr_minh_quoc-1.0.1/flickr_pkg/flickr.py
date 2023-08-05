#!/usr/bin/env python
import requests
import json
import argparse
import os
import hashlib
import enum
import datetime
from langdetect import detect
from flickr_pkg.language_json import language_alpa_1, language_alpa_3
from getpass import getpass
from os import path
import queue
import time
import math


# Waypoint 1: Flickr API Wrapper


class FlickrApi:
    """The class FlickrApi stores these API keys into private attributes of the built object."""

    def __init__(self, consumer_key, consumer_secret):
        self.__string_validate(consumer_key, consumer_secret)
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret

    @staticmethod
    def __string_validate(consumer_key, consumer_secret):
        """Validate consumer_key and consumer_secret

        Arguments:
            consumer_key {str} -- a string of consumer_key
            consumer_secret {str} -- a string of consumer_secret
        """

        if isinstance(consumer_key, str) == False or isinstance(consumer_secret, str) == False:
            raise(ValueError("Consumer key and consumer secret have to be string"))

    # Waypoint 2: Flickr User
    def find_user(self, username):
        """The function find username by calling Flickr API function flickr.people.findByUsername


        Arguments:
                username {string} -- a string of username
        Raise: Exception if there is any error or username is not avalable

        Returns:
                flick_user {obj} -- an Flickuser object
        """

        try:
            get_api_json = requests.get(
                f'https://www.flickr.com/services/rest/?method=flickr.people.findByUsername&api_key={self.__consumer_key}&username={username}&format=json')
        except:
            raise(Exception("An error occurred"))

        # load json from api
        string_json = get_api_json.text[14:-1]
        string_json = json.loads(string_json)
        # get user_name and user_id
        try:
            user_id = string_json["user"]["id"]
            user_name = string_json["user"]["username"]["_content"]
        except:
            raise(ValueError("An error occurred(username is not exist)"))

        return FlickrUser(user_id, user_name)

    # Waypoint 5: Browse the Photos of a Flickr User

    def get_photos(self, user_id, page=1, per_page=100):
        """
        The method get_photo help browse the Photos of a Flickr User

        Arguments:
                user_id {str} -- The identification of a Flickr user.
                page {int} -- An integer representing the page of the user's photostream to return photos. If this argument is omitted, it defaults to 1.
                per_page {int} --  Max 500
        Return:
                The method get_photos returns a tuple of values:
                        flickr_obj_list {list} -- A list of objects FlickrObjects.
                        per_page{int} -- An integer representing the number of pages of per_page photos in the user's photostream.
                        total_photo {int} -- An integer representing the total number of photos in the user's photostream.
        """

        # Validate page and per_page
        self.validate_get_photos(page, per_page)
        # call data from API
        # get_api_data = requests.get(
        #     f"https://www.flickr.com/services/rest/?method=flickr.people.getPhotos&api_key={self.__consumer_key}&user_id={user_id}&page={page}&per_page={per_page}&format=json")
        get_api_data = requests.get(f"https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key={self.__consumer_key}&user_id={user_id}&page={page}&per_page={per_page}&sort=date-posted-asc&format=json")

        string_json = get_api_data.text[14:-1]
        string_json = json.loads(string_json)

        page_count = string_json["photos"]["pages"]
        photo_count = string_json["photos"]["total"]
        flickr_json = string_json["photos"]["photo"]
        # list of flickr object
        flickr_object_list = []

        for flickr_photo in flickr_json:
            photo = FlickrPhoto(flickr_photo['id'], flickr_photo["title"])
            flickr_object_list.append(photo)

        return (flickr_object_list, page_count, photo_count)

    @staticmethod
    def validate_get_photos(page, per_page):
        try:
            page = int(page)
            per_page = int(per_page)

        except:
            raise(ValueError("Page and perpage have to be int"))

        if per_page > 500:
            raise(ValueError("Max perpage is :500"))

    # Waypoint 6: Find Photo Highest Resolution

    def get_photo_sizes(self, photo_id):
        """The function call photosizes data from API

        Arguments:
            photo_id {str} -- a string of photo id

        Returns:
            list_photo_sizes -- a list of size of photo_id
        """

        get_api_data = requests.get(
            f'https://www.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={self.__consumer_key}&photo_id={photo_id}&format=json')
        string_json = get_api_data.text[14:-1]
        string_json = json.loads(string_json)

        list_sizes = string_json["sizes"]["size"]
        list_photo_sizes = []
        for size in list_sizes:
            flick_photo_size = FlickrPhotoSize(
                size["label"], size["width"], size["height"], size["source"])
            list_photo_sizes.append(flick_photo_size)

        return list_photo_sizes


# Waypoint 7: Fetch Photo Description and Comments

    def get_photo_description(self, photo_id):
        """ The instance method get_photo_description to the class FlickrApi that takes an argument photo_id and returns a string representing the description of the photo.

        Arguments:
            photo_id {string} -- a string of phhoto id
        Return:
            description {string} -- a string of description

        """

        get_api_data = requests.get(
            f'https://www.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key={self.__consumer_key}&photo_id={photo_id}&format=json')
        string_json = get_api_data.text[14:-1]
        string_json = json.loads(string_json)

        return(string_json["photo"]["description"]["_content"])

    def get_photo_comments(self, photo_id):
        """The instance method get_photo_comments to the class FlickrApi that takes an argument photo_id and returns a list of strings corresponding to the comments posted to the photo.

        Arguments:
            photo_id {string} -- a string of phhoto id

        Returns:
            text_comment_list {list} -- a list of comments
        """

        get_api_data = requests.get(
            f'https://www.flickr.com/services/rest/?method=flickr.photos.comments.getList&api_key={self.__consumer_key}&photo_id={photo_id}&format=json')
        string_json = get_api_data.text[14:-1]
        string_json = json.loads(string_json)
        
        try:
            comment_list = string_json["comments"]["comment"]
            text_comment_list = []
            for comment in comment_list:
                text_comment_list.append(comment["_content"])
        except:
            text_comment_list = []

        return text_comment_list

# Waypoint 2: Flickr User


class FlickrUser:
    """The class FlickrUser which constructor takes two arguments user_id and username, in this particular order, where:
            user_id (string): Unique identification of a Flickr account (corresponding to the user's NSID).
            username (string): Username of this Flickr account.
    """

    def __init__(self, user_id, username):
        self.__user_id = user_id
        self.__username = username
        self.__best_size = None
        self.__sizes = []

    @property
    def user_id(self):
        return self.__user_id

    @property
    def username(self):
        return self.__username

    @staticmethod
    def from_json(payload):
        """ The argument payload corresponds to a JSON expression with the following structure (cf. the information of a particular as returned by the Flickr API method flickr.people.findByUsername):

        Arguments:
                payload {str} -- string of json expresstion
        """

        try:
            user_id = payload["id"]
            user_name = payload["username"]["_content"]

        except:
            raise(Exception("An error occurred"))

        return FlickrUser(user_id, user_name)


# Waypoint 3: Flickr Photo


class FlickrPhoto:
    """The class FlickrPhoto which constructor takes two arguments photo_id and title, and add a read-only property id that returns the identification of the photo."""

    def __init__(self, photo_id, title):
        self.__id_ = photo_id
        self.__title = title

    @property
    def id(self):
        return self.__id_

    @property
    def title(self):
        """Detect title and locale"""
        try:
            locale = detect(self.__title)
        except:
            locale = "eng" #default eng if cant not detect
        locale = Locale.from_string(locale)
        return Label(self.__title, locale)

    # WP6 ------------
    @property
    def best_size(self):
        return self.__best_size

    @property
    def sizes(self):
        return self.__sizes

    @sizes.setter
    def sizes(self, value):
        self.__sizes = value
        biggest_size = 0
        biggest_size_index = 0
        for index in range(len(self.sizes)):
            calculate_size = self.sizes[index].width * self.sizes[index].height
            if calculate_size > biggest_size:
                biggest_size = calculate_size
                biggest_size_index = index

        self.__best_size = value[biggest_size_index]
    # ---------------
    # WP7----------------------
    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value):
        """ Detect comments locale"""
        list_comments = []
        for comment in value:
            locale = detect(comment)
            locale = Locale.from_string(locale)
            label = Label(comment, locale)
            list_comments.append(label)
        self.__comments = list_comments

    # WP7
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        """ Detect description locale"""
        locale = detect(value)
        locale = Locale.from_string(locale)
        label = Label(value, locale)
        self.__description = label

    @staticmethod
    def from_json(payload):
        """The function takes an argument payload and returns an object FlickrPhoto

        Arguments:
            payload {dict} -- json format

        Returns:
            FlickrPhoto -- a flick photo object
        """

        try:
            photo_id = payload["id"]
            photo_title = payload["title"]
        except:
            raise(Exception("An error occur at FlickPhoto"))

        return FlickrPhoto(photo_id, photo_title)


# Waypoint 4: Localized Photo Title


class Locale:

    """The class Locale that represents a tag respecting RFC 4646. The constructor of this class takes two arguments:
        language_code: A ISO 639-3 alpha-3 code (or alpha-2 code; which will be automatically converted to its equivalent ISO 639-3 alpha-3 code).
        country_code (optional): A ISO 3166-1 alpha-2 code.
    """

    def __init__(self, language_code, country_code=None):
        self.__language_code = language_code
        self.__country_code = country_code

    def __str__(self):
        return f"{self.__language_code}"

    @staticmethod
    def from_string(locale):
        """a ISO 639-3 alpha-3 code (or alpha-2 code), optionally followed by a dash character - and a ISO 3166-1 alpha-2 code. The method from_string returns an object Locale."""

        try:
            if locale in language_alpa_1:
                return(Locale(language_alpa_1[locale][0]))
            elif locale in language_alpa_3:
                return(Locale(locale))
        except:
            raise(Exception("An error orrcured"))


class Label:
    """The class Label that takes two arguments:

        content: humanly-readable textual content of the label.
        locale (optional): an object Locale identifying the language of the textual content of this label, English by default.
    """

    def __init__(self, content, locale=Locale("eng")):
        self.__content = content
        self.__locale = locale

    @property
    def content(self):
        return self.__content

    @property
    def locale(self):
        return self.__locale


# Waypoint 6: Find Photo Highest Resolution

class FlickrPhotoSize:
    """The class FlickrPhotoSize that provides the information of a given size of a photo:

        label: The label representing this size of a photo.
        width: The number of pixel columns of the photo for this size.
        height: The number of pixel rows of the photo for this size.
        url: The Uniform Resource Locator (URL) that references the image files of the photo for this size."""

    def __init__(self, label, width, height, url):
        self.__label = label
        self.__width = width
        self.__height = height
        self.__url = url

    @property
    def label(self):
        return self.__label

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def url(self):
        return self.__url


# Waypoint 8: Command-line Interface Arguments

def get_arguments():
    """

    This script support the command-line parameters defined hereafter. Some parameters are required, some others are optional with default value.

    --username (required): Username of the account of a user on Flickr
    --cache_path (optional): Specify the absolute path where the script saves photos downloaded from Flickr. It defaults to ~/.flickr/.
    --consumer-key (optional): Flickr API key that our script will use to connect to Flickr server;
    --consumer-secret (optional): Flickr API secret that our script will use to encode request to be sent to Flickr server;
    --save-api-keys (optional): Specify whether to save the Flickr API keys for further usage. It defaults to False.
    --image-only (optional): Specify whether the script must only download photos' images. It defaults to False.
    --info-only (optional): Specify whether the script must only download photos' information. It defaults to False.
    --info-level (optional): Specify the level of information of a photo to fetch:
    0 (default): Title only;
    1: Title and description;
    2: Title, description, and comments.
    """

    parser = argparse.ArgumentParser(
        description='Flickr Mirroring', prog='PROG')

    parser.add_argument("--consumer-key",
                        help=" a unique string used by the Consumer to identify itself to the Flickr API", action="store")

    parser.add_argument("--consumer-secret",
                        help="  a secret used by the Consumer to establish ownership of the Consumer Key", action="store")

    parser.add_argument(
        "--save-api-keys", help=" specify whether to save the Flickr API keys for further usage", action="store_true")

    parser.add_argument(
        "--fifo", help=" specify the First-In First-Out method to mirror the user's photostream, from the oldest uploaded photo to the earliest", action="store_true")

    parser.add_argument(
        "--lifo", help=" specify the Last-In First-Out method to mirror the user's photostream, from the earliest uploaded photo to the oldest (default option)", action="store_true")

    # cache-path
    parser.add_argument(
        "--cache-path", help="   specify the absolute path where the photos downloaded from Flickr need to be cached", default="~/.flickr", action="store")

    # image only
    parser.add_argument(
        "--image-only", help="  specify whether the script must only download photos' images", action="store_true")
    # info level
    parser.add_argument("--info-level", action="store", dest="LEVEL", default=0,
                        help="  specify the level of information of a photo to fetch (value between 0 and 2)", type=int)
    # info only
    parser.add_argument(
        "--info-only", help="  specify whether the script must only download photos' information", action="store_true")

    parser.add_argument(
        "--username", help=" username of the account of a user on Flickr to mirror his photostream", required=True, action="store")

    args = parser.parse_args()
    username = vars(args)
    info_level = vars(args)["LEVEL"]

    try:
        info_level = int(info_level)
        if info_level < 0 or info_level > 2:
            raise(ValueError('Info level from 0 - 2'))
    except:
        raise(ValueError('Info level from 0 - 2'))

    cache_path = vars(args)["cache_path"]
    cache_path = os.path.expanduser(cache_path)
    if os.path.isdir(cache_path) == False:
        os.mkdir(cache_path)

    DEFAULT_PATH = os.path.abspath(f"{cache_path}/flickr_keys")

    # save api
    is_save_api = vars(args)["save_api_keys"]
    username = vars(args)["username"]

    if isinstance(username, str):

        try:
            args = read_file_cmd(DEFAULT_PATH, parser)
        except:
            args = write_file_cmd(DEFAULT_PATH, parser, is_save_api)

    return args


def read_file_cmd(DEFAULT_PATH, parser):
    """The function read data from default path

    Arguments:
        DEFAULT_PATH {string} -- string of os path
        parser {obj} -- an parser object
    """

    with open(DEFAULT_PATH, "r") as read_file:

        json_data = json.load(read_file)
        # GET DATA FROM FILE
        input_api_key = json_data['consumer_key']
        input_api_secret = json_data['consumer_secret']

        parser.set_defaults(consumer_key=input_api_key)
        parser.set_defaults(consumer_secret=input_api_secret)
        args = parser.parse_args()

        return args


def write_file_cmd(DEFAULT_PATH, parser, is_save_api):
    """The function write cmd data to file

    Arguments:
        DEFAULT_PATH {string} -- string of os path
        parser {obj} -- an parser object
        is_save_api {bool} -- True if want to save file else False
    """

    input_api_key = getpass('Enter your Flickr API key:')
    parser.set_defaults(consumer_key=input_api_key)
    input_api_secret = getpass('Enter your Flickr API secret:')
    parser.set_defaults(consumer_secret=input_api_secret)
    args = parser.parse_args()

    dict_key_secret = {
        'consumer_secret': input_api_secret,
        'consumer_key': input_api_key
    }

    if is_save_api:
        with open(DEFAULT_PATH, "w") as write_file:
            json.dump(dict_key_secret, write_file)
        os.chmod(DEFAULT_PATH, 0o600)

    return(args)


class CachingStrategy(enum.Enum):
    FIFO = 1
    LIFO = 2
# Waypoint 10: User Photostream Mirroring Agent


class FlickrUserPhotostreamMirroringAgent:
    """The  class FlickrUserPhotostreamMirroringAgent in the script flickr.py which constructor takes the following arguments:

            username (required): Username of the account of a user on Flickr to mirror his photostream.
            flickr_consumer_key (required): A unique string used by the Consumer to identify itself to the Flickr API.
            flickr_consumer_secret (required): A secret used by the Consumer to establish ownership of the Consumer Key.
            cache_root_path_name (optional): Specify the absolute path where the images and/or information of the photos downloaded from Flickr need to be stored in.
            cache_directory_depth (optional): Number of sub-directories the cache file system is composed of, its depth, to store photo files into the child directories, the leaves, of this cache. We will see this parameter later in this mission.
            image_only (optional): Specify whether the script must only download photos' images.
            info_level (optional): Specify the level of information of a photo to fetch (value between 0 and 2)
            info_only (optional): Specify whether the agent must only download photos' information.
    """

    def __init__(self, username, flickr_consumer_key, flickr_consumer_secret, cache_root_path_name="~/.flickr", cache_directory_depth=4, image_only=False, info_level=0, info_only=False, caching_strategy=CachingStrategy.LIFO):

        self.__username = username
        self.__flickr_consumer_key = flickr_consumer_key
        self.__flickr_consumer_secret = flickr_consumer_secret
        self.__cache_root_path_name = cache_root_path_name
        self.__cache_directory_depth = cache_directory_depth
        self.__image_only = image_only
        self.__info_level = info_level
        self.__info_only = info_only
        self.__caching_strategy = caching_strategy
        self.__validate()

    def __validate(self):
        """ Validate  """
        if self.__is_not_tring(self.__username):
            raise(ValueError("Username have to be string"))

        if self.__is_not_tring(self.__flickr_consumer_key):
            raise(ValueError("consumer_key have to be string"))

        if self.__is_not_tring(self.__flickr_consumer_secret):
            raise(ValueError("consumer_secret have to be string"))

        if self.__is_not_tring(self.__cache_root_path_name):
            raise(ValueError("cache_root_path_name have to be string"))

        if self.__is_not_int(self.__cache_directory_depth):
            raise(ValueError("cache_directory_depth have to be int"))

        if self.__cache_directory_depth < 1 or self.__cache_directory_depth > 30:
            raise(ValueError("cache_directory_depth have to be (1 - 30)"))

        if self.__is_not_int(self.__info_level):
            raise(ValueError("info_level have to be int"))

        if self.__info_level > 2 or self.__info_level < 0:
            raise(ValueError("info_level from 0-2"))
        
        if self.__is_not_bool(self.__image_only):
            raise(ValueError("Image only option have to be bool"))
        
        if self.__is_not_bool(self.__info_only):
            raise(ValueError("Info only option have to be bool"))

        if self.__image_only and self.__info_only:
            raise(ValueError("1:( --info-only = True , --image-only = False ) OR 2: (--info-only = False , --image-only = True ) OR 3:(--image-only = False , --image-only = False) "))


    @staticmethod
    def __is_not_tring(value):
        if isinstance(value, str):
            return False
        return True

    @staticmethod
    def __is_not_int(value):
        if isinstance(value, int):
            return False
        return True
    
    @staticmethod
    def __is_not_bool(value):
        if isinstance(value,bool):
            return False
        return True

    @property
    def user(self):
        """ The property user returns an object FlickrUser representing the user whose photostream is going to be mirrored by the instance of the class FlickrUserPhotostreamMirroringAgent.

        Returns:
            FlickrUser {object} -- an object of flickr user
        """

        flickr_api = self.__flickAPI()
        user_obj = flickr_api.find_user(self.__username)

        return FlickrUser(user_obj.user_id, self.__username)

    def run(self):
        """ The funtion download image with Lifo or Fifo strategy """


        #Lifo strategy
        if self.__caching_strategy == CachingStrategy.LIFO:
            self.__lifo()
        #Fifo strategy
        if self.__caching_strategy == CachingStrategy.FIFO:
            self.__fifo()

    def __flickAPI(self):
        """THe function return an object flickAPI

        Returns:
            flickr_api {object} -- an object of flick api
        """


        flickr_api = FlickrApi(self.__flickr_consumer_key,
                               self.__flickr_consumer_secret)
        return flickr_api

    def __lifo(self):
        """The function download image with lifo strategy"""


        user_object = self.user # an object of user
        flickr_api = self.__flickAPI() # call api
        photo_page, photo_per_page = 1, 5
        # Get data from API
        photos, page_count_first, total_image = flickr_api.get_photos(
            user_object.user_id, page=photo_page, per_page=photo_per_page)

        # Save data to check if there is new image feed to sever
        first_total_image = int(total_image)
        # The number of new photo if user feed to sever
        photo_increase = 0
        page_count = page_count_first
        finish = False
      
        try:
            data = self.__read_cache_page()
 
            old_total_image = int(data["total_image"])
            photo_increase_when_reconnect = old_total_image - first_total_image
            new_page_increase_when_reconnect = math.ceil(photo_increase_when_reconnect / photo_per_page)
            print("*------------------------------------------------------------*")
         
            if new_page_increase_when_reconnect == 0:
                page_count = int(data["current_page"] )
    
            else:
                page_count = int(data["current_page"]) - new_page_increase_when_reconnect
                
        except:
            pass
            # page_count = page_number + new_page_increase

        while True:
            #Download from last page to fist page

            if page_count == 1: photo_page = 0
           
            for page_number in reversed(range(photo_page, page_count +1)):
                print(f"Scanning page {page_number}/{page_count_first}")
                #Call API perpage
                photos, new_page_count, new_total_image = flickr_api.get_photos(
                    user_object.user_id, page=page_number , per_page=photo_per_page)
                #Calculate the number of new photo
                photo_increase = int(new_total_image) - first_total_image
                #Calcutate the number of newpage 
                new_page_increase = math.ceil(photo_increase / photo_per_page)
      
                #If there is new photos feed - we download from (current page + new_page increase) to page 1.
                if new_page_increase > 0:
                    #download new_feed
                    #redownload from new index
           
                    page_count = page_number + new_page_increase + 1
                    # page_count = new_page_count
                    page_count_first = new_page_count
                    first_total_image = int(new_total_image)
                    # print(page_count_first,new_page_increase)
                    self.__dowload_new_feed(int(page_count_first),int(new_page_increase),photo_per_page)
                    
                    break
                
                if page_number == 0:
                    finish = True
                    break
 
                if new_page_increase == 0:
                    # lifo download
                    # If there is no photo feed - nomar download 
                    self.__queue_lifo_download(photos)
                    self.__cache_page_lifo(page_number,new_total_image)

          
            if page_count == 0:
               break

            if photo_page == 1 or finish:
                break

    
    
    def __dowload_new_feed(self,total_page,new_page_increase,photo_per_page):
        print("new_feed_________________________________________________________")
        flickr_api = self.__flickAPI()
        user_object = self.user
        for photo_page in reversed(range(total_page-new_page_increase,total_page)):
            print(f"Download new feed : {photo_page + 1}/{total_page}")
            photos, _, _ = flickr_api.get_photos(
                user_object.user_id, page=int(photo_page), per_page=int(photo_per_page))
            self.__queue_lifo_download(photos)
        print("new_feed_end_________________________________________________________")


    # Lifo container
    def __queue_lifo_download(self, photos):
        """ The function get a list of photos
            and download by lifo method

        Arguments:
            photos {list} -- a list of photo
        """

        # create lifo container with max size 4
        max_size = 4
        lifo_container = queue.LifoQueue(max_size)

        for photo in reversed(photos):
            #put photo to container
            lifo_container.put(photo)
            if lifo_container.full:
                photo = lifo_container.get()
                self.download_photo_image(photo)
                # task_done() tells the queue that the processing on the task is complete.
                lifo_container.task_done()

    def __fifo(self):
        """The function dowload image with fifo strategy"""
        
        #get user object
        user_object = self.user
        # Call API
        flickr_api = self.__flickAPI()
        # Min photo page and photo perpage
        photo_page, photos_per_page = 1, 5
        #Get data from API
        photos, page_count, total_image = flickr_api.get_photos(
            user_object.user_id, page=photo_page, per_page=photos_per_page)
        from_page = 0
        from_page = self.__read_cache_page()
        finish = False
        # if from_page >= 1:
        for i in range(0, from_page):
            print(f"Scanning page {i+1}/{page_count}")
            if i == page_count - 1:
                finish = True

        
        while True:
            if finish :
                break
            
            for page_number in range(from_page,page_count):
               
                page = page_number + 1
                
                #read cache
                print(f"Scanning page {page}/{page_count}")
                photos, new_page_count, second_total_image = flickr_api.get_photos(
                    user_object.user_id, page= page, per_page=photos_per_page)

                if second_total_image > total_image:
                    # if new image feed
                    page_count = new_page_count
                    total_image = second_total_image
                    page = page_number

                # QUEUE DOWNLOAD
                if total_image == second_total_image:
                    #cache total image
                    
                    self.__queue_fifo_download(photos)
                    self.__cache_page_fifo(str(page))
                # If have new image feed to flick
                
                
                if page_number == page_count -1:
                    finish = True
                    break
              

    def __queue_fifo_download(self, photos):
        """ The function get a list of photos
            and download by fifo method

        Arguments:
            photos {list} -- a list of photo
        """
        #Create fifo container with maxsize is 4
        max_queue = 4
        photo_queue = queue.Queue(max_queue)
        for photo in photos:
            # Put data to queue
            photo_queue.put(photo)
            if photo_queue.full:
                photo = photo_queue.get()
                self.download_photo_image(photo)
                # task_done() tells the queue that the processing on the task is complete.
                photo_queue.task_done()


    def __cache_page_fifo(self,page_count):
        """The function save downloading page to cached file_fifo

        Arguments:
            page_count {int} -- number of current page
        """

        cached_file_name = "fifo_cached"
        path = os.path.expanduser(self.__cache_root_path_name + "/" + self.__username + "/" + cached_file_name)
        

        with open(path, "w") as write_file:
            write_file.write(str(page_count))
            print("Page cached")

    def __cache_page_lifo(self,page_count,total_image):
        """The function save downloading page to cached file_fifo

        Arguments:
            page_count {int} -- number of current page
        """

        cached_file_name = "lifo_cached"
        path = os.path.expanduser(self.__cache_root_path_name + "/" + self.__username + "/" + cached_file_name)
        data = {}
        data['total_image'] = total_image
        data['current_page'] = page_count

        with open(path, "w") as write_file:
           
            json.dump(data,write_file)
            print("Page cached")
    
    def __read_cache_page(self):
        """ The function return number of downloaded page 

        Returns:
            from_page {int} -- index of page have been cached
        """

        cached_file_name = "fifo_cached"
        if self.__caching_strategy == CachingStrategy.FIFO :
            cached_file_name = "fifo_cached"
        
        if self.__caching_strategy == CachingStrategy.LIFO :
            cached_file_name = "lifo_cached"

        path = os.path.expanduser(self.__cache_root_path_name + "/" + self.__username + "/" + cached_file_name)
        if os.path.isfile(path):
            with open(path, "r") as read_file:
                page = read_file.readline()
                if self.__caching_strategy == CachingStrategy.FIFO:
                    return int(page)
                if self.__caching_strategy == CachingStrategy.LIFO:
                    return json.loads(page)
        
        return 0
                
  
        


# Waypoint 11: Cache Filesystem Structure


    def download_photo_image(self, photo):
        """The private instance method __download_photo_image to the class FlickrUserPhotostreamMirroringAgent that takes a required argument photo (an object Photo). This function downloads the best resolution image of the photo into the local cache using a deep directory structure, under a sub-folder name after the username of the Flickr user.

        Arguments:
            photo {object} -- an object of photo

        """
        # Validate photo object
        if isinstance(photo, FlickrPhoto) == False:
            raise(ValueError("Photo have to be a photo object"))

        flickr_api = FlickrApi(self.__flickr_consumer_key,
                               self.__flickr_consumer_secret)
        

        #get photo url
        sizes = flickr_api.get_photo_sizes(photo.id)
        photo.sizes = sizes
        photo_url = photo.best_size.url
        source_link = photo.id
        hash_source_name = hashlib.md5(source_link.encode(encoding='ascii'))
        # Hash photo id name
        source_link = hash_source_name.hexdigest() + ".jpg"
        json_link = hash_source_name.hexdigest() + ".json"
        # generate deep directory structure
        generate_path = os.path.expanduser(
            self.__cache_root_path_name) + "/" + self.__username
        # cachedfolder   
        json_path = generate_path
        #make folder
        for index in range(len(source_link)):
            if index < self.__cache_directory_depth:
                generate_path += "/" + source_link[index]
                json_path += "/" + json_link[index]

        generate_path += "/"
        json_path += "/"

        try:
            os.makedirs(generate_path)
        except:
            # if directory avalable -> keep going
            pass

        path_image = generate_path + source_link
        path_json = json_path + json_link


        download_both = False
        if self.__image_only == False and self.__info_only == False:
            download_both = True
        #download both / image / info
        while True:
            i = 0
            try:
                if self.__image_only and download_both == False or download_both:
                    
                    r = requests.get(photo_url, allow_redirects=True)
                    print(f"Caching image of photo:{source_link}")
                    #download image
                    self.__write_image_byte(photo_url, path_image)
                    

                if  self.__info_only and download_both == False or download_both :
                    #download json
                    print(f"Caching json data:{json_link}")
                    json_data =  self.__get_json_data(photo,self.__info_level,flickr_api)
                    self.__download_json_info(json_data,path_json)

                break
                
            except:
                i += 1
                time.sleep(0)
                print("Network error: reconnecting")
            if i == 3:
                print("Time out- please check your internet and redownload later")
                break
    
    def __write_image_byte(self,photo_url,path_image):
        """THe function Write image byte to computer

        Arguments:
            photo_url {str} -- link to download the image
            path_image {str} -- folder to save image
        """


        r = requests.get(photo_url, allow_redirects=True)
        #download image
        with open(path_image, "wb") as write_file:
            write_file.write(r.content)
    
    def __download_json_info(self,json_data,path):
        """The function download json_data to computer

        Arguments:
            json_data {dict} -- a dict of json data
            path {str} -- a string of json data
        
        """
        
        with open(path, "w") as write_file:
            write_file.write(str(json_data))

        
    def __get_json_data(self,photo,info_level,flickr_api):
        """

        Arguments:
            photo {obj} -- a photo object
            info_level {int} -- level infomation to fetch from photo
                0 (default): The title of the photo only.
                1: The title and the description of the photo.
                2: The title, the description, and the textual content of the comments of the photo.
            flickr_api {object} -- a flick API object

        Return:
            dict_photo_info{dict} -- return a dict of photo
        """
        
        if info_level == 0:
            
            return self.__title_json(photo)
        elif info_level == 1:
            # title and description
            title = self.__title_json(photo)
            description = self.__description_json(photo,flickr_api)
            merge = {**title, **description}

            return merge
            # return self.
           
        elif info_level == 2:
            # 2: The title, the description, and the textual content of the comments of the photo.
            title = self.__title_json(photo)
            description = self.__description_json(photo,flickr_api)
            comments = self.__comments_json(photo,flickr_api)
            merge = {**title,**description,**comments}

            return merge
    

    @staticmethod
    def __title_json(photo):
        """

        Arguments:
            photo {object} -- an object of photo

        Returns:
            dict_title -- title content and locale of photo
        """
        dict_title = {"title" : { "content" : str(photo.title.content),"locale" : str(photo.title.locale)}}
        return dict_title
    
    @staticmethod
    def __description_json(photo,flickr_api):
        """

        Arguments:
            photo {object} -- photo object
            flickr_api {object} -- flickr api object

        Returns:
            dict_description{object} -- description in for of photo

        """

        photo_description = flickr_api.get_photo_description(photo.id)
        photo.description = photo_description
        dict_description = {"description":{
                    "locale" : str(photo.description.locale),
                    "content" : str(photo.description.content)}}
        return dict_description

    @staticmethod
    def __comments_json(photo,flickr_api):
        """

        Arguments:
             photo {object} -- photo object
            flickr_api {object} -- flickr api object

        Returns:


        """
        comments = flickr_api.get_photo_comments(photo.id)
        dict_comments = {"comments": comments}
        return(dict_comments)
        

        

def main():
    # DEMO WP13

    # mirroring_agent=FlickrUserPhotostreamMirroringAgent(
    #     'manhhai',
    #     '861fa02399dd83d930fac3375c48de7b',
    #     '16b0f2e61a0a8bb6')

    # flickr_api=FlickrApi(
    #     '861fa02399dd83d930fac3375c48de7b', '16b0f2e61a0a8bb6')
    # photo=FlickrPhoto('49674775373', Label(
    #     'Huế 1920-1929 - Chez un grand mandarin : avant le repas', Locale('fra')))

    #Demo WP14
    console_object = vars(get_arguments())
    catching_stategy = CachingStrategy.FIFO

    if console_object['lifo']:
        catching_stategy = CachingStrategy.LIFO
    if console_object['fifo']:
        catching_stategy = CachingStrategy.FIFO

    mirroring_agent = FlickrUserPhotostreamMirroringAgent(
        console_object['username'],
        console_object['consumer_key'],
        console_object['consumer_secret'],
        caching_strategy = catching_stategy,
        image_only = console_object['image_only'],
        info_only = console_object['info_only'],
        info_level = console_object['LEVEL']

    )

    mirroring_agent.run()


if __name__ == "__main__":
    main()
