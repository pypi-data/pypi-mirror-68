#!/usr/bin/env python3
"""Tests case for flickr Api method"""
import pytest
from flickr_photostream.flickr_api import FlickrApi
from flickr_photostream.flickr_model import (
    FlickrPhoto, FlickrPhotoSize, Label)


@pytest.fixture
def flickr_api_object():
    """FlickrApi fixture"""
    key = "fe3a4ac5b4c6b00883b55ffc36d61d5b"
    secrect = "542f483981d6a56d"
    return FlickrApi(key, secrect)


def test_flickrApi_private(flickr_api_object):
    """Test for FlickrApi object"""
    # Private attributes of consumer_key
    with pytest.raises(AttributeError) as excinfor:
        flickr_api_object.consumer_key
        assert "'FlickrApi' object has no attribute 'consumer_key'"\
            in str(excinfor.value)


def test_find_users_method(flickr_api_object):
    """Test method find user"""
    assert flickr_api_object.find_user('manhhai').user_id == '13476480@N07'
    assert flickr_api_object.find_user('manhhai').username == 'manhhai'
    # User Not found
    with pytest.raises(Exception) as exinfor:
        flickr_api_object.find_user('Elena Shumilova')
        assert "User not found" in str(exinfor.value)


def test_get_photos_method(flickr_api_object):
    """ Test method get photos"""
    # Raise Exception in case wrong user_id
    with pytest.raises(Exception) as excinfor:
        flickr_api_object.get_photos('13476480@N0')
        assert "Unknown user" in str(excinfor.value)
    # Best case
    photos, page_count, photo_count = flickr_api_object.get_photos(
        '13476480@N07', page=10, per_page=5)
    assert isinstance(photos[0], FlickrPhoto)
    assert isinstance(photos, list)


def test_get_photo_sizes_method(flickr_api_object):
    """Test get photo size method"""
    size = flickr_api_object.get_photo_sizes('49499522706')
    assert isinstance(size, list)
    assert isinstance(size[0], FlickrPhotoSize)


def test_size_flickr_photo(flickr_api_object):
    """Test update photo size"""
    photos, page_count, photo_count = flickr_api_object.get_photos(
        '13476480@N07')
    photo = photos[0]
    sizes = flickr_api_object.get_photo_sizes(photo.id)
    assert isinstance(photo.title, Label)
    photo.sizes = sizes
    assert isinstance(photo.sizes, list)
    assert isinstance(photo.best_size, FlickrPhotoSize)


def test_description_flickr_api(flickr_api_object):
    """Test method get description"""
    photo_id = '49515206006'
    photo = FlickrPhoto(
        photo_id, 'THU DAU MOT - Ecole des enfants de troupe - La gymnastique -')
    description = flickr_api_object.get_photo_description(photo_id)
    photo.description = description
    assert isinstance(photo.description, Label)
    assert photo.description.content == \
        'Giờ thể dục của học sinh trường Thiếu sinh quân\nBinh Duong – Thu Dau Mot\n    Date : 1920-1929'
    assert str(photo.description.locale) == 'vie'


def test_comments_flickr_api(flickr_api_object):
    """Test method get comments list"""
    photo_id = '8967911298'
    photo = FlickrPhoto(
        photo_id, 'CHOLON 1950 - Vòng xoay giao lộ Khổng Tử - Tổng Đốc Phương (ngã 5 Cholon)')
    comments = flickr_api_object.get_photo_comments(photo_id)
    photo.comments = comments
    assert isinstance(photo.comments, list)
    assert isinstance(photo.comments[0], Label)
    assert photo.comments[0].content == '.\nnơi này thời Pháp thuộc:\n[http://www.flickr.com/photos/13476480@N07/4722795861/]'
    assert str(photo.comments[0].locale) == 'vie'
