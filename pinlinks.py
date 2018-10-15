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

def main(api_token, d=7):
    username, key = api_token.split(':')

    today = datetime.date.today()
    days_ago = today - datetime.timedelta(days=d)
  
    pb = pinboard.Pinboard(api_token)
    posts = pb.posts.all(tag=["recommended"], results=100, fromdt=days_ago)
    
    if not posts:
        print('No articles found!', file=sys.stderr)
        sys.exit(1)

    print('''# ICYMI 웹 탐험 – %s''' % (today.strftime('%Y년 %m월 %d일')))
    print('')
    print('''**기간**: %s ~ %s''' % (days_ago.isoformat(), today.isoformat()))
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
    parser.add_argument('-t', dest='api_token', type=str, help='API token')
    parser.add_argument('-d', dest='days', type=int, help='Since n days')
    args = parser.parse_args()
    main(args.api_token, args.days)
