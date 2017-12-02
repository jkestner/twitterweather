# Global variables and sensitive keys.
# Enter your own config and remove the "-template".

import cgitb
cgitb.enable()
REFRESH_PERIOD = 60*60

MINIMUM_VOLUME = 10

TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""
TWITTER_ACCESS_TOKEN_KEY = ""
TWITTER_ACCESS_TOKEN_SECRET = ""

CACHE_DIR = 'caches/twitter/'
MAP_CACHE_DIR = 'caches/map/'
COMMENT_CACHE_DIR = 'caches/comments/'
