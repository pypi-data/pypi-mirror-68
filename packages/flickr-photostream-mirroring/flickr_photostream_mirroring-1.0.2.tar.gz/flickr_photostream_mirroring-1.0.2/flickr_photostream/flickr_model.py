#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetching Information from Flickr API"""

import logging
import langdetect
from flickr_photostream.constants import ISO_LANGUAGE
from flickr_photostream.exception import NotCorrectFlickrUserInfException

logger = logging.getLogger(__name__)


class FlickrUser:
    """A class Flickr User"""

    def __init__(self, user_id, username):
        """The constructor of FlickrUser

        Args:
            user_id (str):  The user's NSID
            username (str): Username of above Flickr account
        """
        if any([not isinstance(user, str) for user in (user_id, username)]):
            raise NotCorrectFlickrUserInfException(
                "User_id and username must be strings")
        self.__user_id = user_id
        self.__username = username

    @property
    def user_id(self):
        """ Represent to the user's NSID"""
        return self.__user_id

    @property
    def username(self):
        """ Represent to the username of the account"""
        return self.__username

    @staticmethod
    def from_json(payload):
        """Get an object FlickrUser from the provided payload

        Args:
            payload (dic): a JSON expression

        Raises:
            ValueError: `payload` is not dict type
            ValueError: key of `payload` fails expectation VALID_KEY

        Returns:
            FlickrUser Object
        """
        # In case provided data is not a dictionary
        if not isinstance(payload, dict):
            raise ValueError("Data is inappropriate")

        return FlickrUser(payload['id'], payload['username']['_content'])


class FlickrPhoto:
    """A class of Photo"""

    def __init__(self, photo_id, title):
        """The constructor of Flickr Photo

        Args:
            photo_id (str): the Id of the photo
            title (str): title of this photo id
        """
        if any([not isinstance(val, str) for val in (photo_id, title)]):
            raise ValueError("Data is inappropriate")
        self.__id = photo_id
        self.__title = title
        self.__sizes = None
        self.__best_size = None
        self.__description = None
        self.__comments = []
        self.__image_filename = None

    @property
    def id(self):
        """Represent the id of the photo"""
        return self.__id

    @property
    def title(self):
        """Represent the class Label, a humanly-readable textual content
            written in a given locale"""
        return self.__create_label_object(self.__title)

    @property
    def sizes(self):
        """Represent the available sizes of the photo"""
        return self.__sizes

    @sizes.setter
    def sizes(self, val):
        """Setter sizes as val"""
        self.__sizes = val

    def get_resolution(self):
        """Get resolution of the photo"""
        return self.sizes.width * self.sizes.height

    @property
    def best_size(self):
        """Represent the best_size of the photo"""
        return max(self.sizes)

    @best_size.setter
    def best_size(self, val):
        self.__best_size = val

    @property
    def description(self):
        """Represent the description of the photo"""
        return self.__description

    @description.setter
    def description(self, description):
        """Setter description"""
        label = self.__create_label_object(description)
        self.__description = label

    @property
    def comments(self):
        """Represent the comments of the photo"""
        return self.__comments

    @comments.setter
    def comments(self, comments):
        """Setter comments as comments"""
        self.__comments = [
            self.__create_label_object(comment) for comment in comments]

    @property
    def image_filename(self):
        """Hash image filename"""
        return self.__image_filename

    @image_filename.setter
    def image_filename(self, val):
        self.__image_filename = val

    @staticmethod
    def __create_label_object(string):
        try:
            language = langdetect.detect(string)
        except (TypeError, ValueError,
                langdetect.lang_detect_exception.LangDetectException):
            language = "eng"
        return Label(string, Locale(language))

    @staticmethod
    def from_json(payload):
        """Get an object FlickrPhoto from the provided payload

        Args:
            payload (dic): a JSON expression

        Raises:
            ValueError: `payload` is not dict type

        Returns:
            FlickrPhoto Object
        """
        # In case provided data is not a dictionary
        if not isinstance(payload, dict):
            logger.error(
                "Provided data is not dictionary type", exc_info=True)
            raise ValueError("Data is inappropriate")

        return FlickrPhoto(payload['id'], payload['title'])


class Locale:
    """A class of Locale which is handling written language text"""

    def __init__(self, language_code, country_code=None):
        """The construction of Locale class

        Args:
            language_code (str):  A ISO 639-3 alpha-3 code (or alpha-2 code;
                which will be automatically converted to its equivalent
                ISO 639-3 alpha-3 code).
            country_code (str, optional): A ISO 3166-1 alpha-2 code.
                Defaults to None.
        """
        if not isinstance(language_code, str):
            raise ValueError("Data is inappropriate")
        # Parse if '-' in language code
        if "-" in language_code:
            lang_list = language_code.split("-")
            language_code = str(lang_list[0])
            country_code = str(lang_list[1])
        # Automatically converted to its equivalent ISO 639-3
        self.language_code = self.__convert_to_6393alpha3(language_code)
        self.country_code = country_code

    def __str__(self):
        """Override to show a human-readable string presentation
            of the object"""
        if self.country_code:
            return f'{self.language_code}-{self.country_code}'
        return self.language_code

    @staticmethod
    def __convert_to_6393alpha3(language_code):
        # If provided language_code is alpha-2 code, convert it to ISO alpha-3
        if len(language_code) == 2:
            lang_data = ISO_LANGUAGE
            if language_code not in lang_data:
                raise ValueError(
                    f"Do not support for {language_code} language")
            return lang_data[language_code]
        return language_code

    @staticmethod
    def from_string(locale):
        """Get an object Locale

        Args:
            locale (str): a locale.
                An ISO 639-3 alpha-3 code (or alpha-2 code), optionally
                followed by a dash character- and an ISO 3166-1 alpha-2 code.
        """
        return Locale(locale)


class Label:
    """A class Label corresponds to a humanly-readable textual content
        written in a given locale (English by default)."""

    def __init__(self, content, locale=Locale("eng")):
        """The constructor of Label class

        Args:
            content (str): Humanly-readable textual content of the label.
            locale (Locale object, optional): the language of the
                textual content of this label. Defaults to Locale("eng").
        """
        self.__content = content
        self.__locale = locale

    @property
    def content(self):
        """Represent to textual content of the label"""
        return self.__content

    @property
    def locale(self):
        """Represent to the language of the textural content """
        return self.__locale

    @staticmethod
    def to_dict(label_object):
        """Get a dictionary from label object

        Args:
            label_object (Label)

        Returns:
            dict: A dictionary represent to `content` and `locale` of the
                provided object.
                For example: {"content": "Hanoi", locale: ""}
        """
        info_dict = {}
        if not label_object.content:
            info_dict["content"] = ""
            info_dict["locale"] = ""
        else:
            info_dict["content"] = label_object.content
            info_dict["locale"] = str(label_object.locale)
        return info_dict


class FlickrPhotoSize:
    """A Class of Photo Size"""

    def __init__(self, label, width, height, url):
        """The constructor of FlickrPhotoSize

        Args:
            label (str): The label representing this size of a photo.
            width (int): The number of pixel columns of the photo for this size.
            height (int): The number of pixel rows of the photo for this size.
            url (str):  The Uniform Resource Locator (URL) that references
                the image files of the photo for this size.
        """
        self.label = label
        self.width = width
        self.height = height
        self.url = url
        self.resolution = int(self.width) * int(self.height)

    def __eq__(self, other):
        if not isinstance(other, __class__):
            raise ValueError("Not the same object")
        return self.resolution == other.resolution

    def __lt__(self, other):
        if not isinstance(other, __class__):
            return NotImplemented
        return self.resolution < other.resolution

    @staticmethod
    def from_json(payload):
        """Get an object FlickrPhotoSize from the provided payload

        Args:
            payload (dic): a JSON expression

        Raises:
            ValueError: `payload` is not dict type

        Returns:
            FlickrPhotoSize Object
        """
        # In case provided data is not a dictionary
        if not isinstance(payload, dict):
            logger.error(
                "Provided data is not dictionary type", exc_info=True)
            raise ValueError("Data is inappropriate")

        return FlickrPhotoSize(
            payload['label'], int(payload['width']), int(payload['height']),
            payload['source'])
