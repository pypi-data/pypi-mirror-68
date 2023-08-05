#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilities Mirroring Flickr Photostream"""

import logging
import os
import json
logger = logging.getLogger(__name__)


def cache_content_to_file(path_name, content):
    """Cache a list of photo numbers which are downloaded the last times

    Args:
        path_name (str): The path name of cache file
    """
    if not isinstance(path_name, str):
        logger.error("File path name %s is not string type", path_name,
                     exc_info=True)
    # Create and Change chmod to a Secured mode (only accessible by our owner)

    with open(os.open(path_name, os.O_CREAT | os.O_WRONLY, 0o600),
              'w') as _file:
        # Erase old list before caching new list
        _file.seek(0)
        _file.truncate()
        json.dump(content, _file, indent=4, sort_keys=True)


def does_file_exist(filename, directory):
    """Check if a `filename` existed in particular directory or not.

    Args:
        filename (str): file path name
        directory (str): the directory

    Returns:
        bool: `True` if the provided name existed, 'False' otherwise
    """
    if any([not isinstance(name, str) for name in (filename, directory)]):
        logger.error("Given file path name is not string type", exc_info=True)

    for _, _, files in os.walk(directory):
        if filename in files:
            logger.info("%s existed", filename)
            return True
    return False
