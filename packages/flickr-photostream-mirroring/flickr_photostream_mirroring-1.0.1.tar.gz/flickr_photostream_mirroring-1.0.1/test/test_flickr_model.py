#!/usr/bin/env python3
"""Tests case for flickr model"""
import pytest
from flickr_photostream.flickr_api import FlickrApi
from flickr_photostream.flickr_model import (
    FlickrPhoto, FlickrPhotoSize, Label, Locale)
import langdetect


@pytest.fixture
def flickr_api_object():
    """FlickrApi fixture"""
    key = "fe3a4ac5b4c6b00883b55ffc36d61d5b"
    secrect = "542f483981d6a56d"
    return FlickrApi(key, secrect)


def test_FlickrPhoto():
    """Test for FlickrPhoto"""
    payload = {
        "id": "49510908217",
        "owner": "13476480@N07",
        "secret": "6f78f65cfd",
        "server": "65535",
        "farm": 66,
        "title": "SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương",
        "ispublic": 1,
        "isfriend": 0,
        "isfamily": 0
    }
    photo = FlickrPhoto.from_json(payload)
    assert photo.id == "49510908217"


@pytest.fixture
def flickr_photo_size_object():
    """Get fixture FlickrPhotoSize"""
    return FlickrPhotoSize(
        "Original",
        "1533",
        "1600",
        "https://live.staticflickr.com/65535/49499525286_7df8ab7063_o.jpg",
    )


def test_flickr_photo_size_object(flickr_photo_size_object):
    """Test Flickr Photo size object"""
    assert flickr_photo_size_object.label == "Original"
    assert flickr_photo_size_object.width == "1533"
    assert flickr_photo_size_object.height == "1600"
    assert flickr_photo_size_object.url == \
        "https://live.staticflickr.com/65535/49499525286_7df8ab7063_o.jpg"


def test_locale_object():
    """Test Locale object"""
    locale = Locale('vie')
    assert str(locale) == 'vie'
    locale = Locale('vi')
    assert str(locale) == 'vie'
    locale = Locale('fr-CA')
    assert str(locale) == 'fra-CA'
    locale = Locale.from_string('fr-CA')
    assert str(locale) == 'fra-CA'


def test_label_object():
    """Test Label object"""
    label = Label("Hello, World!")
    assert label.content == 'Hello, World!'
    assert isinstance(label.locale, Locale)
    assert str(label.locale) == 'eng'
    label = Label("Rạch Bến Nghé, Bến Chương Dương", Locale('vie'))
    assert label.content == 'Rạch Bến Nghé, Bến Chương Dương'
    assert str(label.locale) == 'vie'


@pytest.fixture
def flickr_photo_object():
    return FlickrPhoto(
        '49510908217', 'SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương')


def test_flickr_photo_object_best_case(flickr_photo_object):
    """Test FlickrPhoto best case"""

    # Best case
    assert isinstance(flickr_photo_object.title, Label)
    assert flickr_photo_object.title.content == \
        'SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương'
    assert isinstance(flickr_photo_object.title.locale, Locale)
    assert str(flickr_photo_object.title.locale) == 'vie'
    assert isinstance(flickr_photo_object.comments, list)

    # Test update comments list
    flickr_photo_object.comments = ["test comment"]
    assert isinstance(flickr_photo_object.comments[0], Label)

    # Test update decriptions
    flickr_photo_object.description = "test desctiption"
    assert isinstance(flickr_photo_object.description, Label)

    # Test update decriptions
    assert flickr_photo_object.image_filename == None
    flickr_photo_object.image_filename = "test image_filename"
    assert isinstance(flickr_photo_object.image_filename, str)


def test_flickr_photo_object_corner_cases():
    """Test FlickrPhoto corner case"""

    with pytest.raises(ValueError) as expinfo:
        incorect_photoid = FlickrPhoto(
            12, 'Rạch Bến Nghé, Bến Chương Dương')
        assert "Data is inappropriate" in str(expinfo.value)

    # Only support for string type
    with pytest.raises(ValueError) as expinfo:
        incorect_title = FlickrPhoto(
            '49510908217', Locale('Rạch Bến Nghé, Bến Chương Dương'))
        assert "Data is inappropriate" in str(expinfo.value)

    # In case langdelect can not detect language
    wrong_language = FlickrPhoto(
        '49510908217', 'd s s s d s f h s d f h s 8 4 e cszczcd')
    assert str(wrong_language.title.locale == 'eng')

@pytest.fixture
def flickr_photo_size_object():
    return FlickrPhotoSize(
        "Original",
        "1533",
        "1600",
        "https://live.staticflickr.com/65535/49499525286_7df8ab7063_o.jpg",
    )


def test_flickr_photo_size_object(flickr_photo_size_object):
    """Test Flickr Photo size object"""
    assert flickr_photo_size_object.label == "Original"
    assert flickr_photo_size_object.width == "1533"
    assert flickr_photo_size_object.height == "1600"
    assert flickr_photo_size_object.url == \
        "https://live.staticflickr.com/65535/49499525286_7df8ab7063_o.jpg"

