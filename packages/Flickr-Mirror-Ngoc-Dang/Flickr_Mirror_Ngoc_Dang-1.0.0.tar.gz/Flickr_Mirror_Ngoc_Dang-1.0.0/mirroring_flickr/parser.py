#!/usr/bin/env python3
"""Modules"""
import argparse
import constants
import os
import logging
import json
from cache_strategy import CachingStrategy
import stat
import getpass
import requests


# Waypoint 8
def path(string):
    """
    A function to check whether
    a string is a path of not. If
    it does not exist
    :param string(str): a string
        represents a path
    """

    # check if the directory is existed
    # path with a tilde symbol(~/) or dot symbol(./)
    # create the directory if it's existed
    if not os.path.exists(os.path.expanduser(string)):
        os.mkdir(os.path.expanduser(string))
    elif not os.path.exists(os.path.abspath(string)):
        os.mkdir(os.path.realpath(string))

    # If existed, simply take that path
    return os.path.realpath(string)


def get_arguments():
    """
    Simply a function to get an Namespace object with attributes related to our
        FlickrApi wrapper
    :return (Namespace): a Namespace objects that hold the arguments passed
        as attributes
    """

    # create ArgumentParser object
    parser = argparse.ArgumentParser(description="Flickr Mirroring")

    # optional arguments
    parser.add_argument(
        "--cache-path",
        help="specify the absolute path where the photos downloaded\
                            from Flickr need to be cached",
        type=path,  # check arguments as path
        default=os.path.realpath(os.path.expanduser('~/.flickr/')))

    parser.add_argument(
        "--info-level",
        help="specify the level of information of a photo to fetch\
                            (value between 0 and 2)",
        choices=range(3),  # only 3 levels allowed
        type=int,
        metavar="LEVEL",
        default=0)

    parser.add_argument(
        "--save-api-keys",
        help="specify whether to save the Flickr API keys for\
                            further usage",
        action="store_true")

    parser.add_argument(
        "--cache-directory-depth",
        help="depth of directory to save",
        type=int,
        metavar="",
        default=4)

    # only 1 download method is selected
    group_download_method = parser.add_mutually_exclusive_group()
    group_download_method.add_argument(
        "--fifo",
        help="specify the First-In First-Out method to mirror the\
                        user's photostream, from the oldest uploaded photo to\
                        the earliest",
        action='store_true')

    group_download_method.add_argument(
        "--lifo",
        help="specify the Last-In First-Out method to mirror the\
                        user's photostream, from the earliest uploaded photo\
                        to the oldest (default option)",
        action='store_true')

    # only 1 dowload data is selected
    group_download_data = parser.add_mutually_exclusive_group()
    group_download_data.add_argument(
        "--image-only",
        help="specify whether the script must only download photos\
                            images",
        action="store_true")

    group_download_data.add_argument(
        "--info-only",
        help="specify whether the script must only download photos'\
                            information",
        action="store_true")

    # required
    parser.add_argument(
        "--username",
        help="username of the account of a user on Flickr to mirror\
                              their photostream",
        required=True)

    args = parser.parse_args()

    # get the path we store the json file
    path_save = args.cache_path + constants.CACHE_FILE

    try:

        # read cached file
        with open(path_save, 'r') as file_save:

            # get the previous used key
            data = json.loads(file_save.read())
            consumer_secret = data['consumer_secret']
            consumer_key = data['consumer_key']

    # if the cached file is not existed
    except FileNotFoundError:
        while True:

            # Waypoint9
            # prompt user to input api key and secret
            consumer_key = \
                getpass.getpass("Enter your Flickr API key:")
            consumer_secret = \
                getpass.getpass("Enter your Flickr API secret:")

            payload = {
                "method": "flickr.test.echo",
                "api_key": consumer_key,
                "format": "json",
                "nojsoncallback": "1"
            }

            test_key = requests.get(constants.END_POINT,
                                    params=payload)
            if json.loads(test_key.text)["stat"] == "fail":
                logging.warning(json.loads(test_key.text)['message'])
            else:
                break

        # if save-api-keys option is selected
        if args.save_api_keys is True:
            if not os.path.exists(constants.DEFAULT_PATH):
                os.mkdir(constants.DEFAULT_PATH)

            # set up file path and data to write
            data_save = {
                "consumer_secret": consumer_secret,
                "consumer_key": consumer_key
            }
            json_object = json.dumps(data_save, indent=4)

            # create file if not existed with w+ mode
            with open(path_save, "w+") as file_save:

                # write data into the file
                file_save.write(json_object)

            # only user can edit the file
            os.chmod(path_save,
                     stat.S_IRUSR |
                     stat.S_IWUSR)

    # set the download stategy
    if args.lifo:

        # lifo if lifo is selected
        strategy = CachingStrategy.LIFO

    elif args.fifo:

        # fifo if lifo is selected
        strategy = CachingStrategy.FIFO

    else:

        # default is lifo
        strategy = CachingStrategy.LIFO

    # check some cases for image only and --info-level
    if args.image_only is True and args.info_level != 0:
        raise parser.error(
            "--image-only is not allowed to have --info-level")

    # return Namespace object
    return argparse.Namespace(cache_path=args.cache_path,
                              image_only=args.image_only,
                              info_level=args.info_level,
                              info_only=args.info_only,
                              username=args.username,
                              consumer_key=consumer_key,
                              consumer_secret=consumer_secret,
                              cache_directory_depth=args.cache_directory_depth,
                              cache_strategy=strategy)
