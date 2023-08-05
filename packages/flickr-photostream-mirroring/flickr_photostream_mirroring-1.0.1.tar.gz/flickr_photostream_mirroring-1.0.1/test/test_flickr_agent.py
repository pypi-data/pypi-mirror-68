#!/usr/bin/env python3
"""Tests case for Agent"""
import pytest
from flickr_photostream.flickr_api import FlickrApi
from flickr_photostream.flickr_model import (
    FlickrPhoto, FlickrPhotoSize, Label, FlickrUser)
from flickr_photostream.flickr_agent import FlickrUserPhotostreamMirroringAgent



def test_flickr_user_photo_stream_mirroring_agent():
    """Test Flickr User Agent"""
    mirroring_agent = FlickrUserPhotostreamMirroringAgent(
        'manhhai',
        'fe3a4ac5b4c6b00883b55ffc36d61d5b',
        '542f483981d6a56d')
    assert isinstance(mirroring_agent.user, FlickrUser)
    assert mirroring_agent.user.user_id == '13476480@N07'
    assert mirroring_agent.user.username == 'manhhai'
    assert mirroring_agent.flickr_consumer_key == 'fe3a4ac5b4c6b00883b55ffc36d61d5b'
    assert mirroring_agent.flickr_consumer_secret == '542f483981d6a56d'
