import nltk
import re

def __parse_words(t):
    '''
    Split the tweet into words. Pull out hashtags, mentions, and links.
    '''
    ht = []
    mt = []
    li = []

    for word in t['text'].split(' '):
        if word.startswith('#'):
            ht.append(word.lower().lstrip('#'))
            continue

        if word.startswith('@'):
            mt.append(word.lower().lstrip('@'))
            continue

        if word.startswith('http'):
            li.append(word)
            continue

    return ht, mt, li            


def __parse_phrases(t, count):
    ngrams = nltk.util.ngrams(t['text'].lower().split(), count)
    return [' '.join(ngram) for ngram in ngrams]


def __parse_time(timestamp):
    '''
    Get the timestamp for the tweet, remove the seconds and minutes, and
    store the timestamp for analysis.
    '''
    m = re.search(r'(\d\d:\d\d:\d\d \+\d\d\d\d)', timestamp)
    if m is not None:
        return re.sub(r':\d\d:\d\d ', ':00:00 ', m.group(1))
    else:
        return None


def __parse_place(place):
    '''
    Capture the place id, country, and full_name.
    '''
    if place is not None:
        return (place['id'], place['country'], place['full_name'])
    else:
        return None


def __parse_coord(tweet):
    coords = tweet.get('coordinates')
    if coords is not None:
        return (tweet['created_at'], tuple(coords['coordinates']))
    else:
        return None


def parse_tweets(tweets):
    analysis = {'hashtags': [], 'mentions': [], 'links': [], 'phrase3': [],
                'phrase4': [], 'phrase5': [], 'times': [], 'places': [],
                'coords': []}

    for tweet in tweets:
        ht, mt, li = __parse_words(tweet)
        analysis['hashtags'].extend(ht)
        analysis['mentions'].extend(mt)
        analysis['links'].extend(li)

        analysis['phrase3'].extend(__parse_phrases(tweet, 3))
        analysis['phrase4'].extend(__parse_phrases(tweet, 4))
        analysis['phrase5'].extend(__parse_phrases(tweet, 5))

        time = __parse_time(tweet['created_at'])
        if time is not None:
            analysis['times'].append(time)

        place = __parse_place(tweet['place'])
        if place is not None:
            analysis['places'].append(place)

        coord = __parse_coord(tweet)
        if coord is not None:
            analysis['coords'].append(coord)

    return analysis
