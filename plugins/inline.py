# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import random
import time
import requests
import json
import bs4
import html5lib
import hds

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle

@pyrogram.Client.on_inline_query()
async def inline(bot, inline_query):
    if inline_query.query == "":
       await inline_query.answer(
                           results=[],
                           cache_time=1,
                           switch_pm_text="🤔🤔🤔 Search anything 👇",
                           switch_pm_parameter="nosearch"
       )
       return
    results = []
    mx5 = []
    u = "https://www.mxplayer.in/?q=" + inline_query.query.replace(" ", "%20") + "&search=true"
    mx1 = requests.get(u, headers=hds.mxplayer)
    mx2 = bs4.BeautifulSoup(mx1.content.decode('utf-8'), "html5lib")
    mx3 = mx2.find_all("body")[0].find_all("a")
    for mx4 in mx3:
      try:
        img = mx4.find_all("img")[0]['src']
        title = mx4.find_all("img")[0]['title']
        result = {
               "title":"{}".format(title),
               "img":"{}".format(img),
               "href":"{}".format(mx4['href'])
        }
        mx5.append(result)
      except:
        pass
    #mx5.pop(0)
    for mx6 in mx5:
           results.append(
              InlineQueryResultArticle(
                  title="{}".format(mx6['title']),
                  thumb_url="{}".format(mx6['img']),
                  input_message_content=InputTextMessageContent(
                      message_text="{}".format(mx6['href'])
                  ),
                  reply_markup=InlineKeyboardMarkup(
                     [ 
                        [
                           InlineKeyboardButton('🔍 Inline here', switch_inline_query_current_chat=''),
                           InlineKeyboardButton('🔍 Other chat', switch_inline_query='')
                        ]
                     ]
                  )
              )
           )
    if results:
     pm_text =  str(len(results)) + " results were found"
     await inline_query.answer(
                        results=results,
                        cache_time=5,
                        switch_pm_text=pm_text,
                        switch_pm_parameter="results"
     )
     return
    else:
      await inline_query.answer(
          results = [],
          cache_time=1,
          switch_pm_text="🙁🤔😐 No results found 😔",
          switch_pm_parameter="noresults"
      )
      return
