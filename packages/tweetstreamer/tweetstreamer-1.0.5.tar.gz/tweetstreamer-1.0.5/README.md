# tweetstreamer

[![CircleCI](https://circleci.com/gh/suddi/tweetstreamer.svg?style=svg)](https://circleci.com/gh/suddi/tweetstreamer)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a3fbed333f5e4d43b6be56a000ea42ca)](https://www.codacy.com/app/suddir/tweetstreamer)
[![PyPI](https://img.shields.io/pypi/v/tweetstreamer.svg?maxAge=2592000)](https://pypi.python.org/pypi/tweetstreamer)
[![PyPI](https://img.shields.io/pypi/wheel/tweetstreamer.svg)](https://pypi.python.org/pypi/tweetstreamer)
[![PyPI](https://img.shields.io/pypi/implementation/tweetstreamer.svg)](https://github.com/suddi/tweetstreamer)
[![license](https://img.shields.io/github/license/suddi/tweetstreamer.svg?maxAge=2592000)](https://github.com/suddi/tweetstreamer)

A Tweepy streamer to collect tweets from Twitter's Streaming API based on criteria, with an extremely simple API

## Requirements

You will need the following from Twitter:

* CONSUMER_KEY
* CONSUMER_SECRET
* ACCESS_KEY
* ACCESS_SECRET

For this you can visit https://apps.twitter.com to setup the access keys

## Install

````
pip install tweetstreamer
````

## Usage

For example if you want to listen for tweets about $AAPL stocks

````
from tweetstreamer import auth, listen

connection = auth(<CONSUMER_KEY>, <CONSUMER_SECRET>, <ACCESS_KEY>, <ACCESS_SECRET>)
listen(connection, <TRACK>, on_status, on_error, on_timeout, on_disconnect)
````
