import sys
import time
import telepot

"""
$ python2.7 skeleton.py <token>

A skeleton for your telepot programs.
"""

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print 'Chat Message:', content_type, chat_type, chat_id

# need `/setinline`
def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print 'Inline Query:', query_id, from_id, query_string

    # Compose your own answers
    articles = [{'type': 'article',
                    'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

    bot.answerInlineQuery(query_id, articles)

# need `/setinlinefeedback`
def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print 'Chosen Inline Result:', result_id, from_id, query_string
    

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.notifyOnMessage({'normal': on_chat_message,
                     'inline_query': on_inline_query,
                     'chosen_inline_result': on_chosen_inline_result})
print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)
