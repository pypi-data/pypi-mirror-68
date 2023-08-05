#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetching Information from Flickr API"""

import logging
import requests
from flickr_photostream.constants import (
    MAX_PHOTOS_PER_PAGE, END_POINT)
from flickr_photostream.exception import NotCorrectFlickrUserInfException
from flickr_photostream.flickr_model import (
    FlickrPhoto, FlickrPhotoSize, FlickrUser)
logger = logging.getLogger(__name__)


class FlickrApi:
    """A Class relate to process Flickr API"""

    def __init__(self, consumer_key, consumer_secret):
        """The constructor of FlickrApi

        Args:
            consumer_key (str): A Flickr member key
            consumer_secret (str): A Flickr menter secrect
        """
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret

    def find_user(self, username):
        """Find Flickr User

        Args:
            username (str): the username of Flickr user

        Raises:
            ValueError: provided user is not a string

        Returns:
            FlickrUser Object
        """
        if not isinstance(username, str):
            logger.error("Username must be a string", exc_info=True)
            raise NotCorrectFlickrUserInfException("Data is inappropriate")
        # Set up paramenters
        param = {"method": "flickr.people.findByUsername", "username": username}
        # Make a get request
        data = self.__get_data_when_call_api(param)
        return FlickrUser.from_json(data['user'])

    def get_photos(self, user_id, page=1, per_page=100):
        """Get information of photos of a particular user

        Args:
            user_id (str): The identification of a Flickr user.
            page (int, optional): An integer representing the page of
                the user's photostream to return photos. Defaults to 1.
            per_page (int, optional): An integer representing the number
                of photos to return per page. Defaults to 100.

        Raises:
            ValueError: page, per_page is not an interger
            ValueError: per_page value > MAX_PHOTOS_PER_PAGE.
            Exception: Fetch data fail, raise the its message

        Returns:
            (tuple): A tuple of values
                A list of objects FlickrObjects.
                An integer representing the number of pages of per_page photos
                    in the user's photostream.
                An integer representing the total number of photos in
                    the user's photostream.
        """
        if any([not isinstance(val, int) for val in (page, per_page)]):
            raise ValueError("Page must be an integer")
        if per_page > MAX_PHOTOS_PER_PAGE:
            raise ValueError(
                f"The number of photos per page must be less than {MAX_PHOTOS_PER_PAGE}")
        # Set up paramenters
        param = {
            "method": "flickr.people.getPhotos",
            "user_id": user_id, "per_page": per_page, "page": page}
        # Make a get request
        data = self.__get_data_when_call_api(param)
        # Parse data
        page_count = int(data['photos']['pages'])
        photo_count = int(data['photos']['total'])
        photos_list = data['photos']['photo']
        # In case user don't have any photos"
        if not photos_list:
            logger.debug("User don't have any photos")
            photos = photos_list
        else:
            photos = [FlickrPhoto.from_json(payload)
                      for payload in photos_list]
        return photos, page_count, photo_count

    def get_photo_sizes(self, photo_id):
        """Get a list of size of the photo

        Args:
            photo_id (str): photo id

        Returns:
            list: a list of objects FlickrPhotoSize
        """
        # Set up paramenters
        params = {"method": "flickr.photos.getSizes", "photo_id": photo_id}
        # Make a get request
        data = self.__get_data_when_call_api(params)
        # Parse data
        photo_size = data['sizes']['size']
        return [FlickrPhotoSize.from_json(payload) for payload in photo_size]

    def get_photo_description(self, photo_id):
        """Get description of the provided photo

        Args:
            photo_id (str): the id of the photo

        Returns:
            str: string represent the description of the photo
        """
        params = {
            "method": "flickr.photos.getInfo",
            "photo_id": photo_id
        }
        data = self.__get_data_when_call_api(params)
        description = data["photo"]["description"]["_content"]
        return description

    def get_photo_comments(self, photo_id):
        """Get comments list of the provided photo id

        Args:
            photo_id (str): The id of the photo

        Returns:
            list: A list of string representing all comments of the provided photo
        """
        params = {
            "method": "flickr.photos.comments.getList",
            "photo_id": photo_id
        }
        data = self.__get_data_when_call_api(params)
        comments_dict = data["comments"]
        if 'comment' in comments_dict:
            comments_list = comments_dict["comment"]
        if 'comment' not in comments_dict or not comments_list:
            logger.debug("%s don't have any comments", photo_id)
            return []
        return [comment["_content"] for comment in comments_list]

    def __get_data_when_call_api(self, param):
        # API Calling to get data
        # Set up paramenters
        parameters = {
            "api_key": self._consumer_key,
            "format": "json", "nojsoncallback": 1}
        parameters.update(param)
        # Set up parameters
        response = requests.get(END_POINT, params=parameters)
        # Get a result json
        data = response.json()
        logger.debug(
            'Result of %s %s', parameters["method"], data['stat'], exc_info=True)
        # If the returns is fail, raise an exception
        if data['stat'] == 'fail':
            logger.error(
                'Result of %s %s', parameters["method"], data['message'],
                exc_info=True)
            raise Exception(data['message'])
        return data
