#!/usr/bin/env python
"""
pinlinks.py

Generate Markdown blog post from pinboard public saves.
"""
from configparser import ConfigParser
from datetime import date
import argparse
import calendar
import os
import pinboard
import sys


def main(api_token, y=None, m=None):
    today = date.today()
    year = y if y is not None else today.year
    month = m if m is not None else today.month
    day = calendar.monthrange(year, month)[1] if (y is not None and
                                                  m is not None) else today.day
    print('''---
title: Links for the month of %s
---''' % (date(year, month, 1).strftime('%B %Y'), ))
    for i in range(1, day + 1):
        nenne = date(year, month, i)
        pb = pinboard.Pinboard(api_token)
        posts = pb.posts.get(dt=nenne)
        shared = [post for post in posts['posts'] if post.shared]
        if not posts.get('posts'):
            sys.exit(0)
        elif len(shared) > 0:
            print('\n**%s:**\n' % (nenne.strftime('%A, %B %d %Y'), ))
        for post in shared:
            print('* [%s](%s)' %
                  (post.description.encode('utf-8'), post.url.encode('utf-8')))
            # //pinboard.in/u:%s/b:%s = (user, post.hash[:12].encode('utf-8'))
            if post.extended:
                print('-- %s' % (post.extended.decode('utf-8'), ))


if __name__ == '__main__':
    config = ConfigParser()
    config.read(os.path.expanduser('~/.pinboardrc'))
    api_token = config.get('authentication', 'api_token')
    parser = argparse.ArgumentParser(description='pinlinks')
    parser.add_argument('-y', dest='year', type=int, help='year')
    parser.add_argument('-m', dest='month', type=int, help='month')
    args = parser.parse_args()
    main(api_token, args.year, args.month)
