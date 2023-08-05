"""Modules"""
import logging
import hashlib
import os
import stat
import json
import re
from mirroring_flickr.parser import get_arguments
from langdetect.lang_detect_exception import LangDetectException
from langdetect import detect
from mirroring_flickr.cache_strategy import CachingStrategy
import mirroring_flickr.constants as constants


# a simple function to check str data
def check_input(*argv):
    """
    An function to check str
        elements exclusively
    :return: an error exception
        if one is not string type
    """
    for arg in argv:
        if not isinstance(arg, str):
            raise ValueError(
                "invalid input type")


# WayPoint1
class FlickrApi:
    """FlickrApi wrapper class"""

    def __init__(self, consumer_key, consumer_secret):
        """The constuctor of FlickrApi takes 2 arugments
            which are consumer_key and consumer_secret
            :param consumer_key(str): a string represents an api
                key permitted by Flickr
            :param consumer_secret(str): a secret represents secret
                permitted by Flickr"""

        # validations
        check_input(consumer_key, consumer_secret)

        # all must be private attributes
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret

    # WayPoint2

    def find_user(self, username):
        """
        An instance method that send a request
            request to the Flickr's API endpoint
            to fetch the information about the user
            specified by username
        :param username(str): a string value
            represents username of a Flickr user
        :return: a FlickrUser object
        """

        # Validation
        check_input(username)

        # set up quries for method
        payload = {
            "method": "flickr.people.findByUsername",
            "api_key": self.__consumer_key,
            "username": username,
            "format": "json",
            "nojsoncallback": "1"
        }

        # send request with findByUsername method
        response = constants.SESSION.get(constants.END_POINT, params=payload)

        # parse json data
        data = json.loads(response.text)
        if data['stat'] == 'fail':
            raise Exception("an error occurred")

        # return FlickrUser object
        return FlickrUser.from_json(data['user'])

    # WayPoint5

    def get_photos(self, user_id, page=1, per_page=100):
        """
        An instance method that takes 3 arguments
            user_id, page, per_page that returns
            a tuple of list of FlickrObjects, the number
            of pages in the user's photostream and the total
            number of photos in the user's photostream
        :param user_id(str): a string represents user id
        :param page(int): an integer represents the page
            number to get the photos
        :param per_page(int): an integer represents the number
            of photos to fetch
        """

        # validations for inputs
        if not isinstance(user_id, str):
            raise TypeError(
                "User id must be a string type")
        if not isinstance(page, int):
            raise TypeError(
                "page number must be an integer")
        if per_page not in range(501):
            raise ValueError(
                "per page must be an integer ranged from 100 to 500")

        # params and containers
        list_result = []
        payload = {
            "method": "flickr.people.getPhotos",
            "api_key": self.__consumer_key,
            "user_id": user_id,
            "page": page,
            "per_page": per_page,
            "format": "json",
            "nojsoncallback": "1"
        }

        # request with flickr.people.getPhotos method
        response = constants.SESSION.get(constants.END_POINT, params=payload)

        # get data fetched of photos
        data = json.loads(response.text)

        # raise exception if method fails
        if data['stat'] == 'fail':
            raise Exception("an error occurred")

        for photo in data['photos']['photo']:

            # create FlickrPhoto objects
            list_result.append(
                FlickrPhoto(photo['id'],
                            photo['title']))

        # return tuple of values
        return (list_result,
                data['photos']['pages'],
                data['photos']['total'])

    # WayPoint6

    def get_photo_sizes(self, photo_id):
        """
        An instance method that get information
            about a Flickr photo
        :param photo_id(str): a id of a Flickr
            photo
        :return: a list of FlickrPhotoSize
            objects
        """

        # validations
        check_input(photo_id)

        # set up request method
        # and other queries
        payload = {
            "method": "flickr.photos.getSizes",
            "api_key": self.__consumer_key,
            "photo_id": photo_id,
            "format": "json",
            "nojsoncallback": "1"
        }

        # send request and json load data
        response = constants.SESSION.get(constants.END_POINT,
                                         params=payload)
        # print(response.text)
        data = json.loads(response.text)

        # raise exception if the method fail
        if data['stat'] == 'fail':
            raise Exception("an error occurred")

        # create and return a list of FlickrPhotoSize objects
        list_result = []
        for keys in data['sizes']['size']:
            list_result.append(FlickrPhotoSize(keys['label'],
                                               keys['width'],
                                               keys['height'],
                                               keys['source']))
        return list_result


    # Waypoint7
    def get_photo_description(self, photo_id):
        """
        An instance method that takes 1 arugment
            and return a description of a photo.
            This function use flickr.photos.getInfo
            method of Flickr rest Api
        :param photo_id(str): id of the photo needs to
            get information
        :return(list): a description of a photo fetched
            through Flickr Api method
        """
        # validate inputs
        check_input(photo_id)

        # set up params
        payload = {
            "method": "flickr.photos.getInfo",
            "api_key": self.__consumer_key,
            "photo_id": photo_id,
            "format": "json",
            "nojsoncallback": "1"
        }

        # send request with repaired params
        response = constants.SESSION.get(constants.END_POINT, params=payload)

        # json load response
        data = json.loads(response.text)

        # check if method response is fail or not
        if data['stat'] == "fail":
            raise Exception("an error occurred")

        # return description value
        return json.loads(response.text)['photo']['description']['_content']


    # Waypoint7
    def get_photo_comments(self, photo_id):
        """
        An instance method that takes 1 arugment
            and return a list of comments of a photo.
            This function use the method,
            flickr.photos.comments.getList,
            of Flickr rest Api
        :param photo_id(str): id of the photo needs to
            get information
        :return(list): a list contains comments on the
            photo fetched
        """
        # validate inputs
        check_input(photo_id)

        # set up params
        payload = {
            "method": "flickr.photos.comments.getList",
            "api_key": self.__consumer_key,
            "photo_id": photo_id,
            "format": "json",
            "nojsoncallback": "1"
        }

        # send request with repaired params
        response = constants.SESSION.get(constants.END_POINT, params=payload)

        # json load response
        data = json.loads(response.text)

        # check if method response is fail or not
        if data['stat'] == "fail":
            raise Exception("an error occurred")

        # return description value
        list_result = []
        try:
            for comments in data['comments']['comment']:
                list_result.append(comments['_content'])

        # if no key comment
        # we add an emty list
        finally:
            return list_result


# WayPoint2
class FlickrUser:
    """Class for Flicker user info"""

    def __init__(self, user_id, username):
        """The constructor of FlickrUser takes
            2 arguments which are user_id and
            username
        :param user_id(str): a string represents
            a user id on Flickr
        :param username(str): a string represents
            a username of a Flickr's user
        """

        # validation
        check_input(user_id, username)

        # private attributes
        self.__user_id = user_id
        self.__username = username

    @property
    def user_id(self):
        """Property of user_id attribute """
        return self.__user_id

    @property
    def username(self):
        """Property of username attribute"""
        return self.__username

    @staticmethod
    def from_json(payload):
        """
        An static method that takes
            an arugment payload, which
            corresponds to a JSON expression
            contains information about a user
        :param payload(dict): a JSON expression
        :return: a FlickrUser object created
            by infomation from payload
        """
        return FlickrUser(payload['id'],
                          payload['username']['_content'])


# WayPoint3
class FlickrPhoto:
    """Class represents the FlickrPhoto"""

    def __init__(self, photo_id, title):
        """
        The constructor of FlickrPhoto takes
            2 arguments
        :param photo_id(str): a string represents
            an id of a Flickr photo
        :param title(str): a string represents
            the title of a photo on Flickr
        """

        # validation for the inputs
        check_input(photo_id, title)

        # private attributes
        self.__photo_id = photo_id
        self.__title = title
        self.__sizes = list()
        self.__comments = list()
        self.__description = None

    @property
    def id(self):
        """property of id attribute"""
        return self.__photo_id

    @property
    def title(self):
        """property of title attribute"""
        try:
            localce_iso_693_3 = \
                Locale(constants.ISO_639_1_TO_3[detect(self.__title)])

            # return a Label object
            return Label(self.__title, localce_iso_693_3)

        except LangDetectException:
            return Label(self.__title)

    @staticmethod
    def from_json(payload):
        """
        An static method that parase a JSON format data and create FlickrPhoto
            object
        :param payload(dict): a dictionary that includes information about
            a photo on Flickr
        :return: a FlickrPhoto object
        """
        return FlickrPhoto(payload['id'],
                           payload['title'])

    @property
    def sizes(self):
        """property sizes of FlickPhoto instance"""
        return self.__sizes

    @property
    def best_size(self):
        """property best_size of FlickPhoto instance"""
        try:
            return sorted(self.sizes, reverse=True)[0]
        except IndexError:
            pass

    @property
    def description(self):
        """A property about Photo description"""
        return self.__description

    @property
    def comments(self):
        """A property about photo comments"""
        return self.__comments

    @property
    def image_filename(self):
        """A property about a image file name"""

        # split file name and extension
        _, extension = os.path.splitext(
            self.best_size.url.split('/')[-1])

        # hash file name with md5
        hashed_file_name = \
            hashlib.md5(self.id.encode('utf-8')).hexdigest()

        # return file name
        return f"{hashed_file_name}{extension}"

    @property
    def json_filename(self):
        """
        property of file as json extension
        """
        file_name, _ = \
            os.path.splitext(self.image_filename)

        return f"{file_name}.json"

    @comments.setter
    def comments(self, list_comment):
        """
        setter for property comments
        :param list_comment(list): a list of
            strings
        """

        # validations
        if not isinstance(list_comment, list):
            raise TypeError("Input must be a list")

        list_final = []
        for comment in list_comment:

            if not isinstance(comment, str):
                raise TypeError(
                    "Input must be a list of string")

            try:
                # simply detect the locale of comments
                localize = Locale(
                    constants.ISO_639_1_TO_3[detect(comment)])

                # create and then append to a list
                list_final.append(Label(comment, localize))

                # assign comment attributes with list of objects

            # resolve comments with empty string
            except LangDetectException:
                list_final.append(Label(comment))

        # return list of comments
        self.__comments = list_final

    @description.setter
    def description(self, description_string):
        """
        setter for property description
        :param description_string(str): a
            string represents photo description
        """

        # validation
        check_input(description_string)

        try:
            # detect the locale of the description
            localize = \
                Locale(constants.ISO_639_1_TO_3[detect(
                    description_string)])

            # assignment the attribute with a Label object
            # created from the detected locale and description
            self.__description = Label(description_string,
                                       localize)

        # resolve description with empty string
        except LangDetectException:
            self.__description = Label(description_string)

    @sizes.setter
    def sizes(self, size_list):
        """setter of property sizes
        :param size_list(str):a string represents"""

        # validation
        if not isinstance(size_list, list):
            raise TypeError("Input must be a list")
        for size_item in size_list:
            if not isinstance(size_item, FlickrPhotoSize):
                raise TypeError(
                    "Input must be a list of FlickrPhotoSize")

        self.__sizes = size_list


# WayPoint4
class Locale:
    """Class for locale of a photo title"""

    def __init__(self, language_code, country_code=None):
        """
        Constructor of Locale class:
        :param language_code(str): language code of the title which is in iso
            639-3 format, it can also be iso 639-2 format and then convert to
            iso 639-3 format
        :param country_code(str): Optional arugment that
            is in ISO 3166-1 alpha-2 code format, which
            reprsent a country
        """
        # validation for language code
        if language_code not in constants.ISO_639_1_TO_3.values() \
                and language_code not in constants.ISO_639_1_TO_3.keys():
            raise ValueError("Invalid language code")

        # validation for country code
        if country_code is None:
            country_code = ""
        else:
            if country_code not in constants.ALPHA_2_CODE:
                raise ValueError("country code not exists")

        # validation for str type
        check_input(language_code, country_code)

        # maping language code to iso 639-3
        # as well as setting attributes
        try:
            self.language_code = \
                constants.ISO_639_1_TO_3[language_code]
        except KeyError:
            self.language_code = language_code
        finally:
            self.country_code = country_code

    # string represents the Locale instance
    def __str__(self):
        """string repsesents locale instance"""
        if self.country_code != "":
            return self.language_code + "-" + self.country_code
        return self.language_code

    @staticmethod
    def from_string(locale):
        """
        This static takes 1 argument, which represent a locale and return a
            Locale object
        :param locale: a string representation of a locale, an ISO 639-3
            alpha-3 code (or alpha-2 code), optionally followed by a dash
            character - and an ISO 3166-1 alpha-2 code.
        :return: a Locale object
        """

        # check locale format
        locale_check = re.compile('^[a-z]{2,3}(?:-[A-Z]{2,3})?$')
        if locale_check.match(locale) is not None:
            try:
                locale_list = locale.split('-')
                return Locale(locale_list[0], locale_list[1])
            except IndexError:
                return Locale(locale)
        else:
            raise Exception("Invalid locale input")


# WayPoint4
class Label:
    """Class for title of a photo"""

    def __init__(self, content, locale=Locale('eng')):
        """
        Constructor of Locale class:
        :param content(str): Humanly-readable textual content of the label
        :param locale(Locale): An object Locale identifying the language of
            the textual content of this label (English by default)
        """

        # validation for the input types
        if not isinstance(content, str):
            raise TypeError("content must be string type")
        if not isinstance(locale, Locale):
            raise ValueError("local must be Locale object")

        # private attributes
        self.__content = content
        self.__locale = locale

    @property
    def content(self):
        """property of content attribute"""
        return self.__content

    @property
    def locale(self):
        """property of locale attribute"""
        return self.__locale


# WayPoint6
class FlickrPhotoSize:
    """Class strores data about a photo"""

    def __init__(self, label, width, height, url):
        """
        Constructor of FlickPhotoSize:
        :param label(str): the label representing the size of a photo
        :param width(str): the number of pixel columns of the photo for
            this size
        :Param height(str): the number of pixel rows of the photo for
            this size
        :param url(str): the url that references the image file of the
            photo for this size
        """

        # private attributes
        self.__label = label
        self.__width = width
        self.__height = height
        self.__url = url

    def __lt__(self, other):
        """less than rich comparison"""
        if self.resolution < other.resolution:
            return True

    @property
    def label(self):
        """property label of instance"""
        return self.__label

    @property
    def width(self):
        """property width of instance"""
        return self.__width

    @property
    def height(self):
        """property height of instance"""
        return self.__height

    @property
    def url(self):
        """property url of instance"""
        return self.__url

    @property
    def resolution(self):
        """property of picture resolution"""
        return int(self.height) * int(self.width)


# WayPoint10
class FlickrUserPhotostreamMirroringAgent:
    """Class indicates the minrror agent"""

    def __init__(self,
                 username,
                 flickr_consumer_key,
                 flickr_consumer_secret,
                 cache_root_path_name=None,
                 cache_directory_depth=None,
                 image_only=None,
                 info_level=None,
                 info_only=None,
                 caching_strategy=CachingStrategy.LIFO):
        """
        constructor of the instance:
        username (str): Username of the account of a user on Flickr
            to mirror their photostream.
        flickr_consumer_key (str): A unique string used by the
            Consumer to identify themselves to the Flickr API.
        flickr_consumer_secret (str): A secret used by the Consumer
            to establish ownership of the Consumer Key.
        cache_root_path_name (str): Specify the absolute path
            where the images and/or information of the photos
            downloaded from Flickr need to be stored.
        cache_directory_depth (integer):
            Number of sub-directories the cache file system
        image_only (optional):
            Specify whether the script must only download photos
            images.
        info_level (optional): Specify the level of information of a
            photo to fetch (value between 0 and 2)
        info_only (optional): Specify whether the agent must only
            download photos' information.
        caching_strategy (Enum): an item of enumeration CachingStrategy
        """

        # Ecapsulation
        self.__username = username
        self.__flickr_consumer_key = flickr_consumer_key
        self.__flickr_consumer_secret = flickr_consumer_secret
        self.__cache_root_path_name = cache_root_path_name
        self.__cache_directory_depth = cache_directory_depth
        self.__image_only = image_only
        self.__info_level = info_level
        self.__info_only = info_only
        self.__api_set = FlickrApi(flickr_consumer_key,
                                   flickr_consumer_secret)
        self.__caching_strategy = caching_strategy

    @property
    def user(self):
        """property as an FlickUser object"""
        return self.__api_set.find_user(self.__username)


    # Waypoint11
    def __download_photo_image(self, photo):
        """
        A private method to download photos
        :param photo(FlickrPhoto): a object of FlickrPhoto to use to download
        :param path(str): a path to save the downloaded photo
        :param depth(integer): a integer indicates the level of the path dept
            to create
        """

        # get sizes of the photo
        sizes = self.__api_set.get_photo_sizes(photo.id)

        # set the sizes for the photo
        photo.sizes = sizes

        # create path with username
        file_path = os.path.join(self.__cache_root_path_name,
                                 self.__username)

        # create path with depth
        for i in photo.image_filename[:self.__cache_directory_depth]:
            file_path = os.path.join(file_path, i)

        # create file path
        photo_path = os.path.join(file_path, photo.image_filename)

        # skip download files
        if not os.path.exists(photo_path):

            logging.info(
                f"Caching image of photo {photo.image_filename}")

            # make directories with depth
            os.makedirs(file_path, exist_ok=True)

            # get method for photo
            response = constants.SESSION.get(photo.best_size.url)

            # save photo
            with open(photo_path, 'wb') as file:
                file.write(response.content)

        else:
            logging.info(
                f"Image photo {photo.image_filename} has been download before")


    def __download_info(self, photo):
        """
        An private instance method similar to __donwload_image method, which
        create json to save data(title, description and comments)
        :param photo (Flickrphoto): a photo to fetch data
        """

        # only fetch if best_size is not yet available
        if photo.best_size is None:

            # get sizes of the photo
            sizes = self.__api_set.get_photo_sizes(photo.id)

            # set the sizes for the photo
            photo.sizes = sizes

        # create path with username
        file_path = os.path.join(self.__cache_root_path_name,
                                 self.__username)

        # create path with depth
        for i in photo.image_filename[:self.__cache_directory_depth]:
            file_path = os.path.join(file_path, i)

        # create json path
        json_path = os.path.join(file_path, photo.json_filename)

        # same with download image
        if not os.path.exists(json_path):
            os.makedirs(file_path, exist_ok=True)
            logging.info(f"Caching info of photo {photo.image_filename}")

            # create json file based on info level
            with open(json_path, "w+", encoding='utf-8') as json_file:
                payload = {
                    "title": {
                        "content": photo.title.content,
                        "locale": str(photo.title.locale)
                    }
                }
                # info level 0
                if self.__info_level == 0:

                    # only write photo title with its locale
                    json_file.write(json.dumps(payload, indent=4, ensure_ascii=False))

                else:

                    # write photo description and locale of description
                    description = \
                        self.__api_set.get_photo_description(photo.id)
                    photo.description = description
                    payload['description'] = \
                        {
                            "locale": str(photo.description.locale),
                            "content": photo.description.content
                        }
                    # get title and description for level 1
                    if self.__info_level == 1:
                        json_file.write(json.dumps(payload, indent=4, ensure_ascii=False))

                    # get all data for level 2
                    elif self.__info_level == 2:
                        comments = \
                            self.__api_set.get_photo_comments(photo.id)
                        photo.comments = comments
                        payload['comments'] = list()
                        for i in photo.comments:
                            dict_format = dict()
                            dict_format.setdefault("locale", str(i.locale))
                            dict_format.setdefault("content", i.content)
                            payload['comments'].append(dict_format)
                        json_file.write(json.dumps(payload, indent=4, ensure_ascii=False))

        # tell the user if an infor has been recorded before
        else:
            logging.info(
                f"Info of photo {photo.image_filename} has been download before")

    def run(self):
        """
        An instance method starts to
        mirroring the user's photostream
        """

        # get the total pages first
        _, page_count, total = \
            self.__api_set.get_photos(
                self.user.user_id, page=1, per_page=100)

        # set logging level to info
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s')

        # download with lifo method
        if self.__caching_strategy is CachingStrategy.LIFO:
            self.__download_lifo(page_count)

        # download with fifo method
        elif self.__caching_strategy is CachingStrategy.FIFO:
            self.__download_fifo(page_count)


    # first in first out function
    def __download_fifo(self, page_count):
        """
        An instance method alow user to download from the first published to the
            most recent
        :param page_count (int): the total of pages calculate based on the total of
            photos over the number of photos per page
        """

        # path of json to cache page and image index
        path = os.path.join(
            self.__cache_root_path_name, f"{self.user.username}.json")

        # state of fifo jumping page
        fifo_jumping = False

        # get info from the cache
        if os.path.exists(path):
            fifo_jumping = True
            with open(path, 'r') as cache_file:

                # take sresume page and image index
                data = json.loads(cache_file.read())
                continue_number = data['index']
                last_page_original = data['page']

        else:
            # start with last page
            last_page_original = page_count

        # ends after first page
        while last_page_original >= 1:

            logging.info(f"Scanning page {last_page_original}/{page_count}")

            # downloading the photos
            photos, _, _ = \
                self.__api_set.get_photos(self.user.user_id,
                                          page=last_page_original,
                                          per_page=100)

            # download the last image
            # from the last page
            if fifo_jumping is True:
                photo = continue_number
            else:
                photo = 0

            # recorded the file index
            number_file = 0

            # same downloaded method
            while photo < len(photos):

                # reverse the photo list to get last image of last page
                photo_image = list(reversed(photos))[photo]

                # download based on image only and info only
                if self.__image_only is True:
                    self.__download_photo_image(photo_image)

                elif self.__info_only is True:
                    self.__download_info(photo_image)

                else:
                    self.__download_photo_image(photo_image)
                    self.__download_info(photo_image)

                photo += 1
                number_file += 1

                # write data on each download for later jump
                with open(path, 'w+') as file_cache:
                    payload = {
                        "index": number_file,
                        "page": last_page_original
                        }
                    file_cache.write(json.dumps(payload, indent=4))

                # only user can edit the file
                os.chmod(path,
                         stat.S_IRUSR |
                         stat.S_IWUSR)

            # moving to next page
            # till first page
            fifo_jumping = False
            last_page_original -= 1


    # last in last out function
    def __download_lifo(self, page_count):
        """
        An private instance method that allows user to download from
            the lastest photo to the oldest
        :page_count (int): the total page based on perpage
        """
        # start from first page
        for i in range(1, page_count+1):

            logging.info(f"Scanning page {i}/{page_count}")

            # downloading the photos
            photos, page_count, _ = \
                self.__api_set.get_photos(self.user.user_id,
                                          page=i,
                                          per_page=100)
            for photo in photos:
                if self.__image_only is True:
                    self.__download_photo_image(photo)
                elif self.__info_only is True:
                    self.__download_info(photo)
                else:
                    self.__download_photo_image(photo)
                    self.__download_info(photo)

