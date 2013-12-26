import nltk
import re
import sys
import json

import twanalyze.twitter

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------
def print_distribution(title, words, top=20, ngram=False):
    '''
    Calculate the frequency distribution of the list of words. Print the 20
    most frequent words in the list.
    '''
    if len(words) != 0:
        print title
        print '=' * len(title)

        dist = nltk.FreqDist(words)

        for k in dist.keys()[:top]:
            if ngram is True:
                key = ' '.join(k)
            else:
                key = k

            print u'{0} - {1}'.format(key, dist[k])

        print


def print_user():
    print screen_name
    print '=' * len(screen_name)
    print u'Name: {0}'.format(user['name'])
    print u'Description: {0}'.format(user['description'])
    print 'Location: {0}'.format(user['location'])
    print 'Time Zone: {0}'.format(user['time_zone'])
    print 'UTC Offset: {0}'.format(user['utc_offset']/3600)
    print 'Tweets: {0}'.format(user['statuses_count'])
    print 'Favorites: {0}'.format(user['favourites_count'])
    print 'Listed: {0}'.format(user['listed_count'])
    print 'Followers: {0}'.format(user['followers_count'])
    print 'Following: {0}'.format(user['friends_count'])
    print 


def parse_words(t):
    '''
    Split the tweet into words. Pull out hashtags, mentions, and links.
    '''
    for word in t.split(' '):
        if word == '':
            continue

        if word.startswith('#'):
            hashtags.append(word.lower())
            continue

        if word.startswith('@'):
            mentions.append(word.lower())
            continue

        if word.startswith('http'):
            links.append(word)
            continue            


def parse_time(timestamp):
    '''
    Get the timestamp for the tweet, remove the seconds and minutes, and
    store the timestamp for analysis.
    '''
    m = re.search(r'(\d\d:\d\d:\d\d \+\d\d\d\d)', timestamp)
    if m is not None:
        times.append(re.sub(r':\d\d:\d\d ', ':00:00 ', m.group(1)))


def parse_place(place):
    '''
    Capture the place id, country, and full_name.
    '''
    if place is not None:
        p = (place['id'], place['country'], place['full_name'])
        places.append(p)


def parse_tweet(t):
    '''
    Parse the tweet into separate words, bigrams, and trigrams.
    '''
    parse_words(t['text'])
    parse_time(t['created_at'])
    parse_place(t['place'])
    phrase3.extend(nltk.util.ngrams(t['text'].lower().split(), 3))
    phrase4.extend(nltk.util.ngrams(t['text'].lower().split(), 4))
    phrase5.extend(nltk.util.ngrams(t['text'].lower().split(), 5))


def load_configuration(filename):
    with open(filename) as config_file:
        return json.loads(config_file.read())


#-----------------------------------------------------------------------------
# Main Program
#-----------------------------------------------------------------------------
if len(sys.argv) != 2:
    print 'Usage: twanalyze screen_name'
    sys.exit()

cfg = load_configuration('twanalyze.config')
tw = twanalyze.twitter.Twitter(cfg['consumer_key'], cfg['consumer_secret'],
                     cfg['token'], cfg['token_secret'])
stats = {'replies': 0, 'favorited': 0, 'retweeted': 0}
hashtags = []
mentions = []
links = []
phrase3 = []
phrase4 = []
phrase5 = []
times = []
places = []

screen_name = sys.argv[1]
user = tw.user(screen_name)
tweets = tw.tweets(screen_name)

for tweet in tweets:
    parse_tweet(tweet)

print_user()
print_distribution('Hashtags', hashtags)
print_distribution('Mentions', mentions)
print_distribution('Links', links)
print_distribution('3-word Phrases', phrase3, ngram=True)
print_distribution('4-word Phrases', phrase4, ngram=True)
print_distribution('5-word Phrases', phrase5, ngram=True)
print_distribution('Timestamps', times)
print_distribution('Places', places)
