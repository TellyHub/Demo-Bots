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
    headers = {
         "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:80.0) Gecko/20100101 Firefox/80.0",
         "Referer":"https://www.tamilyogi.best",
         "Accept":"*/*",
         "Accept-Encoding":"gzip, deflate, br",
         "Accept-Language":"en-US,en;q=0.9",
         "Origin":"https://www.tamilyogi.best",
         "Connection":"keep-alive",
         "sec-fetch-dest":"empty",
         "sec-fetch-mode":"cors",
         "sec-fetch-site":"same-site",
    }
    if inline_query.query == "":
       await inline_query.answer(
                           results=[],
                           cache_time=1,
                           switch_pm_text="🤔🤔🤔 Search anything 👇",
                           switch_pm_parameter="nosearch"
       )
       return
    results = []
    u = "http://tamilyogi.best/?s=" + inline_query.query.replace(" ", "+") + "&submit=Search"
    ty1 = requests.get(u, headers=headers)
    ty2 = bs4.BeautifulSoup(ty1.content.decode('utf-8'), "html5lib")
    ty3 = ty2.find_all("a")
    for ty4 in ty3:
         logger.info(ty4)
         for resulttt in ts4:
          if "Watch Online" in resulttt:
           results.append(
              InlineQueryResultArticle(
                  title="{}".format(resulttt),
                  input_message_content=InputTextMessageContent(
                      message_text="<b>{}</b>".format(ty4['href'])
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
