#!/usr/bin/env python
"""
pinlinks.py

Generate Markdown blog post from pinboard saves.
"""
from configparser import ConfigParser
import datetime
import argparse
import pinboard
import sys


def main(api_token, d=7):
    today = datetime.date.today()
    days_ago = today - datetime.timedelta(days=d)
  
    pb = pinboard.Pinboard(api_token)
    posts = pb.posts.all(tag=["recommended"], results=100, fromdt=days_ago)
    
    if not posts:
        print('No articles found!', file=sys.stderr)
        sys.exit(1)

    print('''# ICYMI 웹 탐험일지 – %s''' % (today.strftime('%Y년 %m월 %d일')))
    print('')
    print('''기간: %s ~ %s''' % (days_ago.isoformat(), today.isoformat()))
    print('')
    
    for post in posts:
        if not post.description:
            continue
        print('* [%s](%s)' %
              (post.description, post.url))
        if post.extended:
            print('\t%s' % (post.extended, ))

if __name__ == '__main__':
    config = ConfigParser()
    parser = argparse.ArgumentParser(description='pinlinks')
    parser.add_argument('-t', dest='api_token', type=str, help='API token')
    parser.add_argument('-d', dest='days', type=int, help='Since n days')
    args = parser.parse_args()
    main(args.api_token, args.days)
