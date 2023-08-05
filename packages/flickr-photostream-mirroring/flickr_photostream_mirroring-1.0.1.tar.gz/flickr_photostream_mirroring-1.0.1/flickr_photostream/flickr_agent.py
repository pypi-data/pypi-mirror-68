#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mirroring Flickr User Photostream"""

import logging
import json
import os
from enum import Enum
import hashlib
import queue
import requests
from flickr_photostream.constants import (
    DEFAULT_CACHE_PATH, LEVEL_DICT, DOWNLOADED_PHOTOS_NAME)
from flickr_photostream.flickr_api import FlickrApi
from flickr_photostream.utils import (
    cache_content_to_file, does_file_exist)
logger = logging.getLogger(__name__)


class CachingStrategy(Enum):
    """A class support for enumerations with members FIFO LIFO

    Args: Enum:
        FIFO: First-In First-Out method consists of downloading photos
            from the oldest published by the user to the most recent.
        LIFO: Last-In First-Out method consists in downloading photos
            from the most recent photo published by the user to the oldest.
    """
    FIFO = 1
    LIFO = 2


class FlickrUserPhotostreamMirroringAgent:
    """A class FlickrUserPhotostreamMirroringAgent"""
    IMAGES_PER_PAGE = 8

    def __init__(
            self, username, flickr_consumer_key, flickr_consumer_secret,
            cache_root_path_name=DEFAULT_CACHE_PATH, image_only=False,
            info_level=0, info_only=False, verify_image=False,
            caching_strategy=CachingStrategy.LIFO):
        """The constructor of FlickrUserPhotostreamMirroringAgent

        Args:
            username (str): Username of the account of a user on Flickr to
                mirror their photostream.
            flickr_consumer_key (str): A unique string used by the Consumer
                to identify themselves to the Flickr API.
            flickr_consumer_secret (str): A secret used by the Consumer to
                establish ownership of the Consumer Key.
            cache_root_path_name (str, optional): Specify the absolute path
                where the images and/or information of the photos.
                Defaults to DEFAULT_CACHE_PATH.
            cache_directory_depth (int, optional): Number of sub-directories
                the cache file system is composed of (i.e., its depth,
                to store photo files into the child directories, the leaves,
                of this cache). Defaults to 4.
            image_only (bool, optional): Specify whether the script must
                only download photos' images. Defaults to False.
            info_level (int, optional): Specify the level of information
                of a photo to fetch (value between 0 and 2). Defaults to 0.
            info_only (bool, optional): Specify whether the agent must only
                download photos' information. Defaults to False.
            verify_image (bool, optional): Specify whether the script must
                verify images that have been download. Defaults to False.
            downloaded_photos(list, optional): A list of photos which are
                downloaded
            is_photo_fetching(bool, optional): Specify whether the script must
                download photos' images. Defaults to True.
            is_info_caching(bool, optional): Specify whether the script must
                fetch photos' information. Defaults to True.
        """

        self.username = username
        self.flickr_consumer_key = flickr_consumer_key
        self.flickr_consumer_secret = flickr_consumer_secret
        self.cache_root_path_name = cache_root_path_name
        self.cache_directory_depth = 4
        self.caching_strategy = caching_strategy
        self.image_only = image_only
        self.info_only = info_only
        self.info_level = info_level
        self.verify_image = verify_image

        self.flickr_api = FlickrApi(
            self.flickr_consumer_key, self.flickr_consumer_secret)
        self.__user = self.flickr_api.find_user(self.username)

        # Define is_info_caching and is_photo_fetching
        self.is_photo_fetching = not self.info_only
        self.is_info_caching = not self.image_only

        self.downloaded_photos = []

    @property
    def user(self):
        """Represent the FlickrUser - the user whose photostream is
            going to be mirrored """
        return self.__user

    def run(self):
        """ Download and cache photos information according to
            the specified caching strategy"""

        if self.caching_strategy == CachingStrategy.FIFO:
            # Method FIFO: reading a user's photostream from their first
            # published photos to the most recent
            pages_queue = queue.Queue()
            photos_queue = queue.Queue()
        else:
            # Method LIFO: reading a user's photostream from their most
            # recent published photo to their first published photos
            pages_queue = queue.LifoQueue()
            photos_queue = queue.LifoQueue()

        # Create a cache file which contains a list of photo numbers which
        # are downloaded in the first time downloaded.
        # If it existed, read information to update attribute downloaded_photos
        downloaded_path_file = os.path.join(
            *[self.cache_root_path_name, self.username, DOWNLOADED_PHOTOS_NAME])
        if os.path.exists(downloaded_path_file):
            with open(downloaded_path_file, 'r') as _file:
                data = json.load(_file)
                self.downloaded_photos = data

        # Start download image or cache photo information followed FIFO/LIFO methods
        try:
            self.mirror_photo(pages_queue, photos_queue)
        except (KeyboardInterrupt, SystemExit) as exc:
            logger.error('%s', exc)
        except Exception as exc:
            logger.error('%s', exc, exc_info=True)
        finally:
            # Always cache a list of photos which have been downloaded last time
            # to files
            cache_content_to_file(downloaded_path_file, self.downloaded_photos)

    # Update sizes, best_size, description, comments, image_filename
    def __update_photo_info(self, photo):

        # Update photo.sizes
        if not photo.sizes:
            photo.sizes = self.flickr_api.get_photo_sizes(photo.id)

        # Update write to image_filename
        # Hash file name followed MD5
        if not photo.image_filename:
            url = photo.best_size.url
            file_type = str(url.split(".")[-1])
            hash_file_name = '.'.join(
                [hashlib.md5(bytes(photo.id, 'utf-8')).hexdigest(), file_type])
            photo.image_filename = hash_file_name

        # No need upload description and comment when the user
        # only want to download images
        if self.image_only is False:
            # Update photo description
            if self.info_level in (
                    LEVEL_DICT["TITLE_DESCRIPTION"],
                    LEVEL_DICT["TITLE_DESCRIPTION_COMMENT"]):
                if not photo.description:
                    photo.description = self.flickr_api.get_photo_description(
                        photo.id)

            if self.info_level == LEVEL_DICT["TITLE_DESCRIPTION_COMMENT"]:
                # Update photo comments
                if not photo.comments:
                    photo.comments = self.flickr_api.get_photo_comments(
                        photo.id)

    # Create deep directory structure to save Json and image files
    # Returns the deepest path
    def __create_directory_tree(self, hash_file_name):
        depth_lst = list(hash_file_name[:self.cache_directory_depth])
        directory = os.path.join(self.cache_root_path_name, self.username)

        for char in depth_lst:
            directory = os.path.join(directory, char)
            os.makedirs(directory, exist_ok=True)
        return directory

    # Read title, description, and comments of the photo and add to a dictionary
    def __get_photo_info_dictionary(self, photo):
        photo_info_dict = {}
        photo_info_dict["title"] = photo.title.to_dict(photo.title)
        if self.info_level in (LEVEL_DICT["TITLE_DESCRIPTION"],
                               LEVEL_DICT["TITLE_DESCRIPTION_COMMENT"]):
            photo_info_dict["description"] = photo.description.to_dict(
                photo.description)
        if self.info_level == LEVEL_DICT["TITLE_DESCRIPTION_COMMENT"]:
            photo_info_dict["comments"] = []
            for comment in photo.comments:
                photo_info_dict["comments"].append(comment.to_dict(comment))

        return photo_info_dict

    # Cache all info (title, description, and comments of the photo as
    # a dictionary) to a json file
    def __cache_photo_info_to_json_file(self, photo):
        # Make sure create a deep directory tree first
        directory = self.__create_directory_tree(photo.image_filename)

        # Get the file name path of the json file
        file_name = "".join([photo.image_filename.split(".")[0], ".json"])
        json_path = os.path.join(directory, file_name)

        # Cache the information (a dictionary) of the photo to json file
        logger.info("Caching information of the photo %s",
                    photo.image_filename)
        content = self.__get_photo_info_dictionary(photo)
        with open(json_path, "w", encoding='utf-8') as json_file:
            json.dump(content, json_file, ensure_ascii=False, indent=4)

    # Download the best resolution image of the photo into the local cache
    #     using a deep directory structure, under a sub-folder named after
    #     the username of the Flickr user.
    # Args: photo (Photo Object)
    def __download_photo_image(self, photo):
        hash_file_name = photo.image_filename
        url = photo.best_size.url
        # Create deep directory structure to save file
        downloaded_path = self.__create_directory_tree(hash_file_name)

        # Download photo
        logger.info("Caching image of photo %s", hash_file_name)
        response = requests.get(url)
        with open(os.path.join(downloaded_path, hash_file_name), "wb") as _file:
            _file.write(response.content)

    def mirror_photo(self, page_queue, photo_queue):
        """Flickr Photo Mirroring

        Args:
            page_queue (queue): A FIFO queue or LIFO queue of pages
            photo_queue (queue): A FIFO queue or LIFO queue of photos per pages
        """
        # Get a directory to save photo downloaded
        directory = os.path.join(self.cache_root_path_name, self.username)
        # Get ingredient
        _, page_count, photo_count = self.flickr_api.get_photos(
            self.user.user_id, per_page=self.IMAGES_PER_PAGE)

        if self.verify_image:
            logger.info('---MODE: VERIFY IMAGES WHICH HAVE BEEN DOWNLOADED---')
            # Get a list of pages which contain photos which are downloaded last times
            downloaded_pages = self.__get_downloaded_pages_last_time(
                photo_count)
            logger.info('Pages which are downloaded %s', downloaded_pages)

        # Add pages to queue
        for page_number in range(page_count, 0, -1):
            page_queue.put(page_number)

        while not page_queue.empty():
            page_num = page_queue.get()
            # Skip pages which are downloaded last times
            if self.verify_image:
                if page_num in downloaded_pages:
                    logger.info("Photos in page %s have been downloaded. Skip it",
                                page_num)
                    continue

            # Download or caching information of multiple files
            # in the provided queue of photo
            photos, page_count, photo_count = self.flickr_api.get_photos(
                self.user.user_id, page=page_num, per_page=self.IMAGES_PER_PAGE)
            logger.info("Scanning page %s/%s .......", page_num, page_count)

            # Add photos to queue
            for j in range(len(photos)-1, -1, -1):
                # Update size and file name
                self.__update_photo_info(photos[j])
                photo_queue.put(photos[j])
            logger.info("Size of photo queue %s", photo_queue.qsize())

            # Get a list of photos number in pages
            photo_distribution = self.__get_pages_distribution(photo_count)
            photo_list_per_page = photo_distribution[page_num - 1]
            if self.caching_strategy == CachingStrategy.LIFO:
                photo_list_per_page = list(reversed(photo_list_per_page))

            # A queue of photo is ready
            while not photo_queue.empty():
                photo = photo_queue.get()

                # Get the file name path of the json file
                json_name = "".join(
                    [photo.image_filename.split(".")[0], ".json"])
                # Check if the file was downloaded or cached
                if any([does_file_exist(filename, directory) for filename in
                        (photo.image_filename, json_name)]):
                    continue

                # Make decision download photo information or photo image
                if self.is_photo_fetching:
                    self.__download_photo_image(photo)
                if self.is_info_caching:
                    self.__cache_photo_info_to_json_file(photo)

                if self.verify_image:
                    # Add photo which have been downloaded already to downloaded_photos
                    photo_num = photo_list_per_page.pop()
                    if photo_num not in self.downloaded_photos:
                        self.downloaded_photos.append(photo_num)

    # Return a list of pages (follow distributed pages this time)
    # which contain all photos which are downloaded the last time
    def __get_downloaded_pages_last_time(self, photo_count):

        # Get a nested list representing photos in pages
        distributed_photos = self.__get_pages_distribution(photo_count)

        downloaded_photos = self.downloaded_photos
        logger.info('List of photos which are downloaded %s',
                    downloaded_photos)

        # Calculate to find new pages which are downloaded the last times
        distributed_photo_per_page = {}
        for i, chain in enumerate(distributed_photos):
            distributed_photo_per_page[
                i + 1] = list(set(chain) - set(downloaded_photos))
        logging.debug('Pages distributed %s', distributed_photo_per_page)

        # Only return a list of pages (follow distributed pages this time)
        # which contain all photos which are downloaded the last time
        return [page_num for page_num, photos in
                distributed_photo_per_page.items() if not photos]

    # Get a nested list representing photos in pages
    def __get_pages_distribution(self, photo_count):
        photo_numbers = list(range(photo_count, 0, -1))
        distributed_photos = [
            photo_numbers[i: i + self.IMAGES_PER_PAGE]
            for i in range(0, len(photo_numbers), self.IMAGES_PER_PAGE)]
        return distributed_photos
