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

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Referer":"https://www.zee5.com",
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-US,en;q=0.9",
    "Origin":"https://www.zee5.com",
    "Connection":"keep-alive",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-site",
}

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
    u = "https://gwapi.zee5.com/content/getContent/search?q=" + inline_query.query.replace(" ", "%20") + "&start=0&limit=24&asset_type=11&country=IN&languages=en,ta&translation=en&version=5&page=1"
    req2 = requests.get("https://useraction.zee5.com/token/platform_tokens.php?platform_name=web_app").json()["token"]
    headers["X-Access-Token"] = req2
    req1 = requests.get(u, headers=headers).json()
    #logger.info(req1['movies'][0])
    results = []
    detail = []
    try:
        for shows in req1['tvshows']:
            shows = {
                 "thumb":"{}".format(shows.get("image_url")),
                 "title":"{}".format(shows.get("original_title"))
            }
            detail.append(shows)
    except:
        pass
    try:
        for movies in req1['movies']:
            movies = {
                  "thumb":"{}".format(movies.get("image_url")),
                  "title":"{}".format(movies.get("original_title"))
            }
            detail.append(movies)
    except:
        pass
    for result in detail:
           results.append(
              InlineQueryResultArticle(
                  title="{}".format(result['title']),
                  thumb_url="{}".format(result['thumb']),
                  input_message_content=InputTextMessageContent(
                      message_text="testing"
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
