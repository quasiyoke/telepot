# coding=utf8

import asyncio
import time
import threading
import pprint
import sys
import traceback
import random
import telepot
import telepot.async
from telepot.namedtuple import namedtuple, InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultGif, InlineQueryResultVideo

def equivalent(data, nt):
    if type(data) is dict:
        keys = list(data.keys())

        # number of dictionary keys == number of non-None values in namedtuple?
        if len(keys) != len([f for f in nt._fields if getattr(nt, f) is not None]):
            return False

        # map `from` to `from_`
        fields = list([k+'_' if k in ['from'] else k for k in keys])

        return all(map(equivalent, [data[k] for k in keys], [getattr(nt, f) for f in fields]))
    elif type(data) is list:
        return all(map(equivalent, data, nt))
    else:
        return data==nt

def examine(result, type):
    try:
        print('Examining %s ......' % type)

        nt = namedtuple(result, type)
        assert equivalent(result, nt), 'Not equivalent:::::::::::::::\n%s\n::::::::::::::::\n%s' % (result, nt)

        if type == 'Message':
            print('Message glance: %s' % str(telepot.glance(result, long=True)))

        pprint.pprint(result)
        pprint.pprint(nt)
        print()
    except AssertionError:
        traceback.print_exc()
        print('Do you want to continue? [y]', end=' ')
        answer = input()
        if answer != 'y':
            exit(1)


def on_inline_query(msg):
    query_id, from_id, query = telepot.glance(msg, flavor='inline_query')

    if from_id != USER_ID:
        print('Unauthorized user:', from_id)
        return

    examine(msg, 'InlineQuery')
    answerer.answer(msg)


def on_chosen_inline_result(msg):
    result_id, from_id, query = telepot.glance(msg, flavor='chosen_inline_result')

    if from_id != USER_ID:
        print('Unauthorized user:', from_id)
        return

    examine(msg, 'ChosenInlineResult')

    print('Chosen inline query:')
    pprint.pprint(msg)


def compute(inline_query):
    articles = [InlineQueryResultArticle(
                   id='abc', title='HK', message_text='Hong Kong', url='https://www.google.com', hide_url=True),
               {'type': 'article',
                   'id': 'def', 'title': 'SZ', 'message_text': 'Shenzhen', 'url': 'https://www.yahoo.com'}]

    photos = [InlineQueryResultPhoto(
                  id='123', photo_url='https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf', thumb_url='https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf'),
              {'type': 'photo',
                  'id': '345', 'photo_url': 'https://core.telegram.org/file/811140184/1/5YJxx-rostA/ad3f74094485fb97bd', 'thumb_url': 'https://core.telegram.org/file/811140184/1/5YJxx-rostA/ad3f74094485fb97bd', 'caption': 'Caption', 'title': 'Title', 'message_text': 'Message Text'}]

    results = random.choice([articles, photos])
    return dict(results=results, cache_time=20, is_personal=True, next_offset='5')


TOKEN = sys.argv[1]
USER_ID = int(sys.argv[2])

bot = telepot.async.Bot(TOKEN)
answerer = telepot.async.helper.Answerer(bot, compute)
loop = asyncio.get_event_loop()

print('Give me an inline query.')
loop.create_task(bot.messageLoop({'inline_query': on_inline_query,
                                  'chosen_inline_result': on_chosen_inline_result}))
loop.run_forever()
