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

    report = {'user': user, 'tweets': tweets}

    raw = open(filename, 'w')
    raw.write(json.dumps(report, indent=2))
    raw.close()

#-----------------------------------------------------------------------------
# KML REPORT
#-----------------------------------------------------------------------------
def create_kml_report(analysis, filename):
    kml = simplekml.Kml()

    for coord in analysis['coords']:
        kml.newpoint(name=coord[0], coords=[coord[1]])

    if not filename.endswith('.kml'):
        filename = filename + '.kml'

    logging.info('Writing KML report to {0}.'.format(filename))
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
    Calculate the frequency distribution of the list of items. Print the 20
    most frequent items in the list.
    '''
    d = u''
    if len(items) != 0:
        d += '{0}\n'.format(title)
        d += '-' * len(title) + '\n'

        dist = nltk.FreqDist(items)

        for k in dist.keys()[:top]:
            if isinstance(k, tuple):
                key = u' '.join(k)
            else:
                key = k

            d += u'{0} - {1}\n'.format(key, dist[k])

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
    u += '<p>\n' 
    u += u'Name: {0}<br />\n'.format(user['name'])
    u += u'Description: {0}<br />\n'.format(user['description'])
    u += u'Location: {0}<br />\n'.format(user['location'])
    u += 'Time Zone: {0}<br />\n'.format(user['time_zone'])
    u += 'UTC Offset: {0}<br />\n'.format(user['utc_offset']/3600)
    u += 'Tweets: {0}<br />\n'.format(user['statuses_count'])
    u += 'Favorites: {0}<br />\n'.format(user['favourites_count'])
    u += 'Listed: {0}<br />\n'.format(user['listed_count'])
    u += 'Followers: {0}<br />\n'.format(user['followers_count'])
    u += 'Following: {0}<br />\n'.format(user['friends_count'])
    u += '</p>'

    return u.encode('utf-8')


def __html_distribution(title, items, top=20):
    '''
    Calculate the frequency distribution of the list of items. Print the 20
    most frequent items in the list.
    '''
    d = u''
    if len(items) != 0:
        d += '<h2>{0}</h2>\n'.format(title)
        d += '<p>\n'

        dist = nltk.FreqDist(items)

        for k in dist.keys()[:top]:
            if isinstance(k, tuple):
                key = ' '.join(k)
            else:
                key = k

            d += u'{0} - {1}<br />\n'.format(key, dist[k])

        d += '</p>\n'

    return d.encode('utf-8')


def create_html_report(user, analysis, filename):
    if not filename.endswith('.html'):
        filename = filename + '.html'

    logging.info('Writing HTML report to {0}.'.format(filename))

    html = open(filename, 'w')
    html.write('<html>\n<head><meta charset="utf-8"></head>\n<body>\n')
    html.wrtie('<h1>Twanalyze Report</h1>\n')
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
