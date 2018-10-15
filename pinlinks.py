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
import json
import re


re_blockquotes = re.compile(r'^(\s+>|>)\s+(.*)$', re.MULTILINE)

def main(api_token, from_date, to_date=datetime.date.today(), no_random_cover_image=False):
    username, key = api_token.split(':')

    days = (to_date - from_date).days
    if days < 0:
        print('Invalid date range', file=sys.stderr)
        sys.exit(1)

    pb = pinboard.Pinboard(api_token)
    posts = pb.posts.all(tag=["recommended"], results=100, fromdt=from_date)
    
    if not posts:
        print('No articles found!', file=sys.stderr)
        sys.exit(1)

    print('''# ICYMI 웹 탐험 – %s''' % (to_date.strftime('%Y년 %m월 %d일')))
    print('')

    if not no_random_cover_image:
        print('![](https://unsplash.it/1920/1080/?random)')

    print('''**기간**: %s ~ %s''' % (from_date.isoformat(), to_date.isoformat()))
    print('')

    re_blockquotes = re.compile(r'^(\s+>|>)\s+(.*)$', re.MULTILINE)

    # Not note
    pure_posts = [post for post in posts if not post.url.startswith('https://notes.pinboard.in/u:' + username)]

    for post in pure_posts:
        if not post.description:
            continue

        print('* **[%s](%s)**' % (post.description, post.url))

        if post.extended:
            desc = get_desc(post.extended, True)
            print('%s' % (desc, ))

    # Note only
    note_posts = [post for post in posts if post.url.startswith('https://notes.pinboard.in/u:' + username)]

    if note_posts:
        print('')
        print('''## 메모''')
        print('')

    for post in note_posts:
        note_id = post.url.replace('https://notes.pinboard.in/u:' + username + '/', '')

        try:
            fun = pb.notes[note_id]
            response = fun(parse_response=False)
        except pinboard.PinboardServerError as e:
            print("HTTP Error 500: Internal Server Error. Either you have " \
                    "provided invalid credentials or the Pinboard API " \
                    "encountered an internal exception while fulfilling " \
                    "the request.")

            raise e
        else:
            json_response = json.load(response)

            title = json_response['title'] if json_response['title'] else "NO TITLE"
            text = json_response['text']

            print('### [%s](%s)' % (title, post.url))
            print('')

            if text:
                desc = get_desc(text)
                print('%s' % (desc, ))
          
    print('')

def get_desc(extended, as_listitem=False):
    # Remove emtpy lines
    text = "".join([s for s in extended.splitlines(True) if s.strip()])
    text = re.sub(r'(^|[^@\w])@(\w{1,15})\b', r'\1<code>@\2</code>', text)
    if as_listitem:
        text = '\t' + text.replace('\n', '\n\t')
        text = re_blockquotes.sub(r'"\2"', text)

    return text

if __name__ == '__main__':
    config = ConfigParser()
    parser = argparse.ArgumentParser(description='pinlinks')
    parser.add_argument('-A', dest='api_token', type=str, help='API token')
    parser.add_argument('-f', dest='from_date', type=str, help='From')
    parser.add_argument('-t', dest='to_date', type=str, help='To')
    parser.add_argument('-N', dest='no_random_cover_image', type=bool, help='No random cover image')
    args = parser.parse_args()

    from_date = datetime.datetime.strptime(args.from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(args.to_date, '%Y-%m-%d').date()
    main(args.api_token, from_date, to_date, args.no_random_cover_image)
