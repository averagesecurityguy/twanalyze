import simplekml
import nltk
import logging
import json

#-----------------------------------------------------------------------------
# RAW REPORT
#-----------------------------------------------------------------------------
def create_raw_report(user, tweets, filename):
    if not filename.endswith('.json'):
        filename = filename + '.json'

    logging.info('Writing RAW report to {0}.'.format(filename))

    report = {'user': user, 'tweets': tweets}

    raw = open(filename, 'w')
    raw.write(json.dumps(report, indent=2))
    raw.close()


#-----------------------------------------------------------------------------
# KML REPORT
#-----------------------------------------------------------------------------
def create_kml_report(tweets, filename):
    if not filename.endswith('.kml'):
        filename = filename + '.kml'

    logging.info('Writing KML report to {0}.'.format(filename))

    kml = simplekml.Kml()

    for tweet in tweets:
        if tweet['coordinates'] is not None:
            timestamp = simplekml.TimeStamp(when=tweet['created_at'])
            kml.newpoint(name=tweet['id_str'],
                         description=tweet['text'],
                         timestamp=timestamp,
                         coords=[tuple(tweet['coordinates']['coordinates'])])

    kml.save(filename)


#-----------------------------------------------------------------------------
# MARKDOWN REPORT
#-----------------------------------------------------------------------------
def __md_user(user):
    '''
    Print various attributes of the user.
    '''
    u = u''
    u += u'{0}\n'.format(user['screen_name']) 
    u += '-' * len(user['screen_name']) + '\n'
    u += u'Name: {0}\n'.format(user['name'])
    u += u'Description: {0}\n'.format(user['description'])
    u += u'Location: {0}\n'.format(user['location'])
    u += 'Time Zone: {0}\n'.format(user['time_zone'])
    u += 'UTC Offset: {0}\n'.format(user['utc_offset']/3600)
    u += 'Tweets: {0}\n'.format(user['statuses_count'])
    u += 'Favorites: {0}\n'.format(user['favourites_count'])
    u += 'Listed: {0}\n'.format(user['listed_count'])
    u += 'Followers: {0}\n'.format(user['followers_count'])
    u += 'Following: {0}\n'.format(user['friends_count'])
    u += '\n'

    return u.encode('utf-8')


def __md_distribution(title, items, top=20):
    '''
    Calculate the frequency distribution of the list of items. Convert the
    top most frequent items in the list to Markdown
    '''
    d = u''
    if len(items) != 0:
        d += '{0}\n'.format(title)
        d += '-' * len(title) + '\n'

        dist = nltk.FreqDist(items)

        for k in dist.keys()[:top]:
            if title == 'Hashtags':
                link = 'https://twitter.com/search?q=%23{0}'.format(k)
                d += u'* [#{0}]({1}) - {2}\n'.format(k, link, dist[k])
            elif title == 'Mentions':
                link = 'https://twitter.com/{0}'.format(k)
                d += u'* [@{0}]({1}) - {2}\n'.format(k, link, dist[k])
            elif title == 'Links':
                d += u'* [{0}]({0}) - {1}\n'.format(k, dist[k])
            else:
                d += u'* {0} - {1}\n'.format(k, dist[k])

        d += '\n'

    return d.encode('utf-8')


def create_markdown_report(user, analysis, filename):
    if not filename.endswith('.md'):
        filename = filename + '.md'

    logging.info('Writing Markdown report to {0}.'.format(filename))
    
    md = open(filename, 'w')
    md.write('Twanalyze Report\n')
    md.write('================\n')
    md.write(__md_user(user))
    md.write(__md_distribution('Hashtags', analysis['hashtags']))
    md.write(__md_distribution('Mentions', analysis['mentions']))
    md.write(__md_distribution('Links', analysis['links']))
    md.write(__md_distribution('3-word Phrases', analysis['phrase3']))
    md.write(__md_distribution('4-word Phrases', analysis['phrase4']))
    md.write(__md_distribution('5-word Phrases', analysis['phrase5']))
    md.write(__md_distribution('Timestamps', analysis['times'], top=24))
    md.write(__md_distribution('Places', analysis['places']))
    md.close()

#-----------------------------------------------------------------------------
# HTML REPORT
#-----------------------------------------------------------------------------
def __html_user(user):
    '''
    Print various attributes of the user in HTML.
    '''
    u = u''
    u += u'<h2>{0}</h2>\n'.format(user['screen_name'])
    u += '<ul>\n' 
    u += u'<li>Name: {0}</li>\n'.format(user['name'])
    u += u'<li>Description: {0}</li>\n'.format(user['description'])
    u += u'<li>Location: {0}</li>\n'.format(user['location'])
    u += '<li>Time Zone: {0}</li>\n'.format(user['time_zone'])
    u += '<li>UTC Offset: {0}</li>\n'.format(user['utc_offset']/3600)
    u += '<li>Tweets: {0}</li>\n'.format(user['statuses_count'])
    u += '<li>Favorites: {0}</li>\n'.format(user['favourites_count'])
    u += '<li>Listed: {0}</li>\n'.format(user['listed_count'])
    u += '<li>Followers: {0}</li>\n'.format(user['followers_count'])
    u += '<li>Following: {0}</li>\n'.format(user['friends_count'])
    u += '</ul>'

    return u.encode('utf-8')


def __html_distribution(title, items, top=20):
    '''
    Calculate the frequency distribution of the list of items. Print the 20
    most frequent items in the list.
    '''
    d = u''
    if len(items) != 0:
        d += '<h2>{0}</h2>\n'.format(title)
        d += '<ul>\n'

        dist = nltk.FreqDist(items)

        for k in dist.keys()[:top]:
            if title == 'Hashtags':
                link = 'https://twitter.com/search?q=%23{0}'.format(k)
                d += u'<li><a href="{0}">'.format(link)
                d += u'#{0}</a> - {1}</li>\n'.format(k, dist[k])
            elif title == 'Mentions':
                link = 'https://twitter.com/{0}'.format(k)
                d += u'<li><a href="{0}">'.format(link)
                d += u'@{0}</a> - {1}</li>\n'.format(k, dist[k])
            elif title == 'Links':
                d += u'<li><a href="{0}">'.format(k)
                d += u'{0}</a> - {1}</li>\n'.format(k, dist[k])
            else:
                d += u'<li>{0} - {1}</li>\n'.format(k, dist[k])

        d += '</ul>\n'

    return d.encode('utf-8')


def create_html_report(user, analysis, filename):
    if not filename.endswith('.html'):
        filename = filename + '.html'

    logging.info('Writing HTML report to {0}.'.format(filename))

    html = open(filename, 'w')
    html.write('<html>\n<head>\n<meta charset="utf-8">\n')
    html.write('<style type="text/css">\n')
    html.write('h1, h2 {font-family: Georgia, "Times New Roman", serif;}\n')
    html.write('body {font-family: Helvetica, Tahoma, Arial, sans-serif;}\n')
    html.write('li {margin: 0; padding: 0; list-style-type: none;}\n')
    html.write('</style>\n</head>\n<body>\n')
    html.write('<h1>Twanalyze Report</h1>\n')
    html.write(__html_user(user))
    html.write(__html_distribution('Hashtags', analysis['hashtags']))
    html.write(__html_distribution('Mentions', analysis['mentions']))
    html.write(__html_distribution('Links', analysis['links']))
    html.write(__html_distribution('3-word Phrases', analysis['phrase3']))
    html.write(__html_distribution('4-word Phrases', analysis['phrase4']))
    html.write(__html_distribution('5-word Phrases', analysis['phrase5']))
    html.write(__html_distribution('Timestamps', analysis['times'], top=24))
    html.write(__html_distribution('Places', analysis['places']))
    html.write('</body>\n</html>\n')
    html.close()
