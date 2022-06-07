import pytest
from os import sys, path
from fixtures import client

def test_home_page(client):
    
    response = client.get("/")

    assert b'Coordinate Systems Worldwide' in response.data
    assert b'value="search"' in response.data
    assert b'type="search"' in response.data

def test_map(client):
    
    response = client.get("/map")

    assert b'/static/js/map.js' in response.data
    assert b'https://api.maptiler.com/maps/streets/256/tiles' in response.data
    assert b'id="map"' in response.data
    assert b'new MapPage' in response.data

def test_transform(client):
    
    response = client.get("/transform")

    assert b'Online convertor for lat & long coordinates' in response.data
    assert b'value="Transform"' in response.data


def test_about(client):
    
    response = client.get("/about")

    assert b'simplifies discovery of coordinate reference systems' in response.data
    assert b'The main features' in response.data
    assert b'Frequently answered questions' in response.data


def test_gsoc(client):
    
    response = client.get("/gsoc")

    assert b'Google Summer of Code 2015 - Ideas' in response.data
    assert b'Idea #1: EPSG.io improvements' in response.data
    assert b'The mentorship provided by Klokan Technologies GmbH' in response.data


def test_opensearch(client):
    
    response = client.get("/opensearch.xml")

    assert b'<Description>Coordinate systems for spatial reference worldwide</Description>' in response.data
    assert b'<Contact>info@klokantech.com</Contact>' in response.data
    assert b'<moz:SearchForm>http://epsg.io/</moz:SearchForm>' in response.data
