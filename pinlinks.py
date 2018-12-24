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
import requests


re_blockquotes = re.compile(r'^(\s+>|>)\s+(.*)$', re.MULTILINE)

def main(api_token, tags, from_date, to_date=datetime.date.today(), no_random_cover_image=False, no_credit=False):
    username, key = api_token.split(':')

    days = (to_date - from_date).days
    if days < 0:
        print('Invalid date range', file=sys.stderr)
        sys.exit(1)

    pb = pinboard.Pinboard(api_token)
    unique_posts = {}
    for tag in tags: 
        posts = pb.posts.all(tag=tag, results=100, fromdt=from_date)
        for post in posts:
            unique_posts.update({post.url: post})
    posts = unique_posts.values()
    
    if not posts:
        print('No articles found!', file=sys.stderr)
        sys.exit(1)

    print('''# ICYMI 웹 탐험 – %s''' % (to_date.strftime('%Y년 %m월 %d일')))
    print('')

    if not no_random_cover_image:
        r = requests.get('https://unsplash.it/1920/1080/?random')
        print('![]({})'.format(r.url))
        print('')

    print('''**기간**: %s ~ %s''' % (from_date.isoformat(), to_date.isoformat()))
    print('')

    # re_blockquotes = re.compile(r'^(\s+>|>)\s+(.*)$', re.MULTILINE)

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

    if not no_credit:
        print('''> 이 글은 [GitHub - andromedarabbit/pinlinks: Generate a markdown blog post from recent pinboard bookmarks](https://github.com/andromedarabbit/pinlinks)로 자동생성하였습니다''')
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
    parser.add_argument('-T', dest='tags', type=str, help='Comma-separated tags')
    parser.add_argument('-N', dest='no_random_cover_image', type=str, help='No random cover image')
    parser.add_argument('-n', dest='no_credit', type=str, help='No credit')
    args = parser.parse_args()

    tags = [x.strip() for x in args.tags.split(',')]
    if not tags:
        tags = [ "recommended" ]

    from_date = datetime.datetime.strptime(args.from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(args.to_date, '%Y-%m-%d').date()
    no_random_cover_image = json.loads(args.no_random_cover_image.lower()) if args.no_random_cover_image else False
    no_credit = json.loads(args.no_credit.lower()) if args.no_credit else False
    main(args.api_token, tags, from_date, to_date, no_random_cover_image, no_credit)
