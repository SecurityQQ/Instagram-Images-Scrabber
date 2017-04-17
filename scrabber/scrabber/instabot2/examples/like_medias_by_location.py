# coding=utf-8
"""
    instabot example

    Workflow:
        Like medias by location.
"""

import argparse
import os
import sys

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


def like_location_feed(new_bot, new_location, amount=0):
    counter = 0
    max_id = ''
    while counter < amount:
        if new_bot.getLocationFeed(new_location['location']['pk'], maxid=max_id):
            location_feed = new_bot.LastJson
            for media in tqdm(location_feed["items"]):
                if bot.like(media['id']):
                    counter += 1
            if location_feed.get('next_max_id'):
                max_id = location_feed['next_max_id']
            else:
                return False
    return True

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-amount', type=str, help="amount")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('locations', type=str, nargs='*', help='locations')
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)


if args.locations:
    for location in args.locations:
        print(u"Location: {}".format(location))
        bot.searchLocation(location)
        finded_location = bot.LastJson['items'][0]
        if finded_location:
            print(u"Found {}".format(finded_location['title']))

            if not args.amount:
                nlikes = input(u"How much likes per location?")
            else:
                nlikes = args.amount
            like_location_feed(bot, finded_location, amount=int(nlikes))
else:
    location_name = raw_input(u"Write location name:\n").strip()
    bot.searchLocation(location_name)
    if not bot.LastJson['items']:
        print(u'Location was not found')
        exit(1)
    if not args.amount:
        nlikes = input(u"How much likes per location?")
    else:
        nlikes = args.amount
    ans = True
    while ans:
        for n, location in enumerate(bot.LastJson["items"], start=1):
            print(u'{0}. {1}'.format(n, location['title']))
        print('\n0. Exit\n')
        ans = raw_input(u"What place would you want to choose?\n").strip()
        if ans == '0':
            exit(0)
        try:
            ans = int(ans) - 1
            if ans in range(len(bot.LastJson["items"])):
                like_location_feed(bot, bot.LastJson["items"][ans], amount=int(nlikes))
        except ValueError:
            print(u"\n Not valid choice. Try again")
