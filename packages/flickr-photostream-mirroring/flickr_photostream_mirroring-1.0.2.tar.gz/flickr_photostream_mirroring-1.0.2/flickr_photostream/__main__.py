#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetching Information from Flickr API"""

import logging
import time
import json
import os
import getpass
import argparse
import requests
from flickr_photostream.constants import (
    DEFAULT_CACHE_PATH, KEY_FILE_NAME, END_POINT, LOGGING_LEVEL, DEBUG_FILE_NAME)
from flickr_photostream.flickr_agent import (
    FlickrUserPhotostreamMirroringAgent, CachingStrategy)
from flickr_photostream.exception import NotCorrectFlickrUserInfException
from flickr_photostream.utils import cache_content_to_file

def log_to_console(logging_number):
    """Log info as logging level to file and to console

    Args:
        logging_number (int): The number of logging option
    """

    # Always logging to file 'debug.log'
    logging.basicConfig(
        filename=DEBUG_FILE_NAME,
        level=logging.DEBUG,
        filemode='w',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s-%(funcName)s: %(message)s',
        datefmt='%H:%M:%S')

    # Define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(LOGGING_LEVEL[logging_number])
    # Set a format for console use
    logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # Add the handler to the root logger
    logging.getLogger('').addHandler(console)


def get_arguments():
    """Convert argument strings to objects and assign them as attributes of
        the namespace.

    Return:
        An instance ``argparse.Namespace`` corresponding to the
            populated namespace.
    """
    # Initialize parser
    parser = argparse.ArgumentParser(description='Flickr Mirorring')

    # Add optional arguments
    parser.set_defaults(caching_strategy=CachingStrategy.LIFO)
    # Forbid two conflicting options `fifo` and `lifo`
    caching_strategy_group = parser.add_mutually_exclusive_group()
    # FIFO method
    caching_strategy_group.add_argument(
        '--fifo', dest="caching_strategy",
        action="store_const", const=CachingStrategy.FIFO,
        help="specify the First-In First-Out method to mirror the user's\
            photostream, from the oldest uploaded photo to the earliest")
    # LIFO method
    caching_strategy_group.add_argument(
        '--lifo', dest="caching_strategy",
        action="store_const", const=CachingStrategy.LIFO,
        help="specify the Last-In First-Out method to mirror the \
            user's photostream, from the earliest uploaded photo\
            to the oldest (default option)")

    # Cache path
    parser.add_argument(
        '--cache-path', default=DEFAULT_CACHE_PATH, metavar='CACHE PATH',
        help='specify the absolute path where the photos downloaded\
            from Flickr need to be cached')

    # Forbid two conflicting options `--image-only'` and `--info-only`
    caching_options_group = parser.add_mutually_exclusive_group()
    # Download Image only (do not cache information)
    caching_options_group.add_argument(
        '--image-only', default=False, action="store_true",
        help="Specify whether the script must only download photos' images'")
    # Cache information only (do not download image)
    caching_options_group.add_argument(
        '--info-only', default=False, action="store_true",
        help="Specify whether the script must only download photos' information")
    # Level (info)
    parser.add_argument(
        '--info-level', default=0, metavar='LEVEL', type=int, choices=[0, 1, 2],
        help='Specify the level of information of a photo to fetch\
            (value between 0 and 2)')

    # Save api option
    parser.add_argument(
        '--save-api-keys', default=False,
        action="store_true", dest='save_api_keys',
        help='Specify whether to save the Flickr API keys for further usage.')

    # Debug options
    parser.add_argument(
        '--debug', default=3, type=int, metavar='DEBUG',
        help='specify the logging level, value between 0 and 4, from critical to debug')

    parser.add_argument(
        '--verify-image', default=False, action="store_true",
        help="specify whether the script must verify images that have been download"
    )

    # Add positional arguments
    parser.add_argument(
        '--username', required=True,
        help='Username of the account of a user on Flickr')


    return parser.parse_args()


def process_command_line_interface():
    """ Command-line Interface

    Returns:
        tuple: (api_info, args)
            api_info (dict): which stores Flickr Api information
                {"consumer_secret": api_secret, "consumer_key": api_key}
            args (argparse.Namespace): correspond to the populated namespace.
    """
    args = get_arguments()
    # Get the cache path
    cache_path = os.path.expanduser(args.cache_path)
    # Get the path of secured file
    secured_file_path = os.path.join(cache_path, KEY_FILE_NAME)

    # In case the cache file does not exist, read and save it to file
    if not os.path.exists(secured_file_path):
        # Get Key and Secrect Input
        api_info = __process_api_key_secrect_input()
        # Only save api key when user input `--save-api-keys`
        if args.save_api_keys:
            # Create directory if it doesn't exist
            os.makedirs(cache_path, exist_ok=True)
            # # Get input and save to file
            os.umask(0)
            cache_content_to_file(secured_file_path, api_info)
    else:
        # File existed, open file to read Api Key and Secrect
        with open(secured_file_path, 'r') as cache_file:
            api_info = json.load(cache_file)

    return api_info, args


# Check if Api Key input is valid or not.
# Return True if it's valid, False otherwise
def __is_api_key_valid(consumer_key):
    parameters = {
        "api_key": consumer_key,
        "format": "json", "nojsoncallback": 1,
        "method": "flickr.test.null"}
    # Call API with provided consumer key
    data = requests.get(END_POINT, params=parameters).json()
    if data["code"] == 100:
        print(data["message"])
        return False
    return True


# Handle API key and secrect input.
def __process_api_key_secrect_input():
    api_key = getpass.getpass(prompt="Enter your Flickr API key: ")
    # Check if key api is valid or not
    if not __is_api_key_valid(api_key):
        raise NotCorrectFlickrUserInfException("Invalid Flickr API Key")
    api_secret = getpass.getpass(prompt="Enter your Flickr API secret: ")

    # Return a dict of api information
    return {"consumer_secret": api_secret, "consumer_key": api_key}


def main():
    """Run"""
    # Get the arguments CLI
    api_info, args = process_command_line_interface()

    # Parse argument `debug` to set debug level to log into console
    log_to_console(args.debug)

    if args.image_only and args.info_level:
        raise TypeError("Do not input `info_level` and `image_only` at the same time")

    # Get the arguments to create object
    mirroring_agent = FlickrUserPhotostreamMirroringAgent(
        args.username,
        api_info['consumer_key'],
        api_info['consumer_secret'],
        args.cache_path,
        args.image_only,
        args.info_level,
        args.info_only,
        args.verify_image,
        args.caching_strategy)

    mirroring_agent.run()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    logging.info("Finished in %s secs", end - start)
