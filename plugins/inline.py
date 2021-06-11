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
    ty5 = []
    u = "http://tamilyogi.best/?s=" + inline_query.query.replace(" ", "+") + "&submit=Search"
    ty1 = requests.get(u)
    ty2 = bs4.BeautifulSoup(ty1.content.decode('utf-8'), "html5lib")
    ty3 = ty2.find_all("a")
    for ty4 in ty3:
      try:
        img = ty4.find_all("img")[0]['src']
        result = {
               "title":"{}".format(ty4['title']),
               "href":"{}".format(ty4['href']),
               "src":"{}".format(img)
        }
        ty5.append(result)
      except:
        pass
    ty5.pop(0)
    for ty6 in ty5:
           results.append(
              InlineQueryResultArticle(
                  title="{}".format(ty6['title']),
                  thumb_url="{}".format(ty6['src']),
                  input_message_content=InputTextMessageContent(
                      message_text="{}".format(ty6['href'])
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
