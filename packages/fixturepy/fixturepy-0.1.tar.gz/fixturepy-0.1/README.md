# Python data fixtures

[![Build Status](https://travis-ci.org/exentriquesolutions/fixturepy.svg?branch=master)](https://travis-ci.org/github/exentriquesolutions/fixturepy)

Create data fixtures to use them in  your tests

Sample usage:

    >>> from fixturepy import Fixture
    >>> fixture = Fixture()
    >>> fixture.create(int) # create an integer
    20932
    >>> fixture.create(str) # create a string
    '63d0b4e450354948b69f6c3b4f9238f9'
 
