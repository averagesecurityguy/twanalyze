#!/usr/bin/env python
import sys
import json
import logging

import twanalyze.twitter
import twanalyze.report
import twanalyze.parse

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------
def load_configuration(filename):
    with open(filename) as config_file:
        return json.loads(config_file.read())


#-----------------------------------------------------------------------------
# Main Program
#-----------------------------------------------------------------------------
if len(sys.argv) != 4:
    print 'Usage: twanalyze screen_name report_file_name html|kml|md|all'
    sys.exit()

cfg = load_configuration('twanalyze.config')
tw = twanalyze.twitter.Twitter(cfg['consumer_key'], cfg['consumer_secret'],
                     cfg['token'], cfg['token_secret'])

# Get data
screen_name = sys.argv[1]
user = tw.user(screen_name)
tweets = tw.tweets(screen_name)

# Analyze data
analysis = twanalyze.parse.parse_tweets(tweets)

# Report analysis
report_file = sys.argv[2]
format = sys.argv[3].lower()

if format == 'html':
    twanalyze.report.create_html_report(user, analysis, report_file)
elif format == 'kml':
    twanalyze.report.create_kml_report(analysis, report_file)
elif format == 'all':
    twanalyze.report.create_html_report(user, analysis, report_file)
    twanalyze.report.create_kml_report(analysis, report_file)
    twanalyze.report.create_markdown_report(user, analysis, report_file)
else:
    if format != 'md':
        logging.warning('Invalid report format, defaulting to Markdown.')
    twanalyze.report.create_markdown_report(user, analysis, report_file)
