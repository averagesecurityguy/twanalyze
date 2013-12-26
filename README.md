twanalyze
=========

Twanalyze downloads account information and up to 3200 of the most recent tweets for the specified screen_name. The downloaded tweets are analyzed and a report is generated that includes the top 20 hashtags, mentions, links, tweet times, locations, and phrases used in each tweet.

Prerequisites
-------------
Twanalyze is dependent on the [requests](http://docs.python-requests.org/en/latest/index.html) and [nltk](http://nltk.org/) libraries.
* `pip install requests`
* `pip install nltk`

Twanalyze also needs a Twitter API key. You can get an API key by signing in to https://dev.twitter.com/apps with your Twitter username and password. Once you are signed in, click Create a new application.

Configuration
-------------
Once you have obtained the Twitter API key, you will need to add the consumer key, consumer secret, token, and token_secret to the twanalyze.config.template file and rename the file to twanalyze.config.

Usage
-----
python twanalyze.py screen_name
