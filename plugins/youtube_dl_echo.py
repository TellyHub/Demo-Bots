#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import pip
from pip._internal import main as _main

package_names=['html5lib'] #packages to install
_main(['install'] + package_names + ['--upgrade'])

import asyncio
import json
import math
import os
import time
import re
import requests
import bs4
import html5lib
import datetime
import hds

# the secret configuration specific things
from sample_config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import humanbytes
from helper_funcs.help_uploadbot import DownLoadFile
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
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

@pyrogram.Client.on_message(pyrogram.Filters.regex(pattern=".*http.*"))
async def echo(bot, update):
      for users in Config.BOTDB.find():
          user = users.get("user_id")
          plan = users.get("plan_name")
          paid = users.get("paid_on")
          exp = users.get("expire_on")
          if int(update.from_user.id) == int(user):
            if datetime.strptime(exp, '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
              await update.reply_text("Plan Expired!\n\nPlease upgrade to continue...")
              to_be_deleted = {
                "user_id": "{}".format(user),
                "plan_name": "{}".format(plan),
                "paid_on": "{}".format(paid),
                "expire_on": '{}'.format(exp)
              }
              Config.BOTDB.delete_one(to_be_deleted)
              return
            try:
                await bot.get_chat_member(
                chat_id=Config.AUTH_CHANNEL,
                user_id=update.from_user.id
                )
            except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.AUTH_CHANNEL_TEXT,
                    parse_mode="html",
                    reply_to_message_id=update.message_id,
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = '??? Updates Channel', url = "https://t.me/Super_botz")]])
                )
                return
            if update.from_user.id in Config.BANNED_USERS:
                await update.reply_text("You are B A N N E D")
                return
            # logger.info(update)
            #TRChatBase(update.from_user.id, update.text, "/echo")
            await bot.send_chat_action(
                 chat_id=update.chat.id,
                 action="typing"
            )
            logger.info(update.from_user)
            u = update.text
            youtube_dl_username = None
            youtube_dl_password = None
            file_name = None
            url = None
            if "|" in u:
               ul_part = u.strip(" ")
               ul_parts = ul_part.split("|")
               u = ul_parts[0]
            if "aha" in u:
              if "movies" in u:
                ahamovpath = "%2Fmovies%2F" + u.split("movies/")[-1]
                ahareq1 = requests.get("https://prod-api-cached-2.viewlift.com/content/pages?path=" + ahamovpath + "&site=aha-tv&includeContent=true&moduleOffset=0&moduleLimit=5&languageCode=default&countryCode=IN").json()["modules"][1]["contentData"][0]["gist"]["id"]
                try:
                  url = requests.get("https://prod-api.viewlift.com/entitlement/video/status?id=" + ahareq1 + "&deviceType=web_browser&contentConsumption=web", headers=hds.aha).json()["video"]["streamingInfo"]["videoAssets"]["hls"]
                except:
                  await update.reply_text("???? Currently Premium movies are not supported...!")
                  return
              elif "originals" in u:
                ahaorgpath = "%2Foriginals%2F" + u.split("originals/")[-1]
                ahareq1 = requests.get("https://prod-api-cached-2.viewlift.com/content/pages?path=" + ahaorgpath + "&site=aha-tv&includeContent=true&moduleOffset=0&moduleLimit=5&languageCode=default&countryCode=IN").json()["modules"][1]["contentData"][0]["gist"]["id"]
                try:
                  url = requests.get("https://prod-api.viewlift.com/entitlement/video/status?id=" + ahareq1 + "&deviceType=web_browser&contentConsumption=web", headers=hds.aha).json()["video"]["streamingInfo"]["videoAssets"]["hls"]
                except:
                  await update.reply_text("???? Currently Premium Shows are not supported...!")
                  return
            elif "zee5" in u:
              if "zee5vodnd.akamaized.net" in u:
                 await bot.send_message(
                      chat_id=update.chat.id,
                      text=Translation.INVALID_URL,
                      reply_to_message_id=update.message_id,
                      parse_mode="html",
                      disable_web_page_preview=True
                 )
                 return
              elif "tvshows" or "originals" in u:
                 req1 = requests.get("https://useraction.zee5.com/tokennd").json()
                 rgx = u.split("/")[-1:]
                 li = { "url":"zee5vodnd.akamaized.net", "token":"https://gwapi.zee5.com/content/details/" }
                 req2 = requests.get("https://useraction.zee5.com/token/platform_tokens.php?platform_name=web_app").json()["token"]
                 headers["X-Access-Token"] = req2
                 req3 = requests.get("https://useraction.zee5.com/token").json()
                 r2 = requests.get(li["token"] + rgx[0], 
                                                    headers=headers, 
                                                    params={"translation":"en", "country":"IN"}).json()
                 g2 = (r2["hls"][0].replace("drm", "hls"))
                 if "netst" in g2:
                            url = (g2 + req3["video_token"])
                            file_name = r2["title"]
                            thumb = r2["image_url"]
                            duration = r2["duration"]
                            description = r2["description"]
                 else:
                            url = ("https://" + li["url"] + g2 + req1["video_token"])
                            file_name = r2["title"]
                            thumb = r2["image_url"]
                            duration = r2["duration"]
                            description = r2["description"]
              elif "movies" in u:
                 r1 = requests.get(li["token"] + "-".join(rgx),
                                                    headers=headers, 
                                                    params={"translation":"en", "country":"IN"}).json()
                 g1 = (r1["hls"][0].replace("drm", "hls") + req1["video_token"])
                 url = ("https://" + li["url"] + g1)
                 file_name = r1["title"]
                 thumb = r1["image_url"]
                 duration = r1["duration"]
                 description = r1["description"]
            elif "mxplayer" in u:
              if "movie" in u:
                 mx1 = requests.get(u, headers=hds.mxplayer)
                 mx2 = bs4.BeautifulSoup(mx1.content.decode('utf-8'), "html5lib")
                 mx3 = mx2.find_all("script")[1].prettify()
                 G = []
                 for i in mx3.split('"'):
                  if "embed/detail" in i:
                    G.append(i)
                 mx4 = G[0]
                 mx5 = requests.get(mx4[:-1], headers=hds.mxplayer)
                 mx6 = bs4.BeautifulSoup(mx5.content.decode('utf-8'), "html5lib")
                 mx7 = mx6.find_all("script")[0].prettify()
                 H = []
                 O = []
                 N = []
                 for j in mx7.split('"'):
                    if ",.mp4" in j:
                      H.append(j)
                 try:
                    url = H[0]
                 except IndexError:
                    for k in mx7.split('"'):
                      if ".mp4" in k:
                        H.append(k)
                      if ".m3u8" in k:
                        O.append(k)
                      if "hlsurl" in k:
                        N.append(k)
                    try:
                      sampleurl = H[0]
                      url = "https://llvod.mxplay.com/" + O[0]
                    except IndexError:
                      try:
                        sample2url = N[0]
                        url = O[0]
                      except IndexError:
                        await update.reply_text("???? DRM Protected...!")
                        return
                 if "voot" in url:
                   await update.reply_text("???? Voot Videos Temporarily Disabled...!")
                   return
              elif "show" in u:
                 mxs1 = requests.get(u, headers=hds.mxplayer)
                 mxs2 = bs4.BeautifulSoup(mxs1.content.decode('utf-8'), "html5lib")
                 mxs3 = mxs2.find_all("script")[1].prettify()
                 GS = []
                 for ia in mxs3.split('"'):
                  if "embed/detail" in ia:
                    GS.append(ia)
                 try:
                  mxs4 = GS[0]
                  mxs5 = requests.get(mxs4[:-1], headers=hds.mxplayer)
                  mxs6 = bs4.BeautifulSoup(mxs5.content.decode('utf-8'), "html5lib")
                  mxs7 = mxs6.find_all("script")[0].prettify()
                  HSS = []
                  OSS = []
                  NSS = []
                  for sss in mxs7.split('"'):
                    if ",.mp4" in sss:
                      HSS.append(sss)
                  try:
                      url = HSS[0]
                  except IndexError:
                      for kss in mxs7.split('"'):
                        if ".mp4" in kss:
                          HSS.append(kss)
                        if ".m3u8" in kss:
                          OSS.append(kss)
                        if "hlsurl" in kss:
                          NSS.append(kss)
                      try:
                        sssampleurl = HSS[0]
                        url = "https://llvod.mxplay.com/" + OSS[0]
                      except IndexError:
                        try:
                          sample3urll = NSS[0]
                          url = OSS[0]
                        except IndexError:
                          await update.reply_text("???? DRM Protected...!")
                          return
                 except IndexError:
                  HS = []
                  OS = []
                  NS = []
                  for js in mxs3.split('"'):
                    if ",.mp4" in js:
                      HS.append(js)
                  try:
                    url = HS[0]
                  except IndexError:
                    for ks in mxs3.split('"'):
                      if ".mp4" in ks:
                        HS.append(ks)
                      if ".m3u8" in ks:
                        OS.append(ks)
                      if "hlsurl" in ks:
                        NS.append(ks)
                    try:
                      ssampleurl = HS[0]
                      url = "https://llvod.mxplay.com/" + OS[0]
                    except IndexError:
                      try:
                        sample2url = NS[0]
                        url = OS[0]
                      except IndexError:
                        await update.reply_text("???? DRM Protected...!")
                        return
              elif "live-tv" or "music-online" in u:
                 await update.reply_text("???? Now only Support Movies & Shows...!")
                 return
            elif "tamilyogi" in u:
                 ty1 = requests.get(u)
                 ty2 = bs4.BeautifulSoup(ty1.content.decode('utf-8'), "html5lib")
                 ty3 = ty2.find_all("iframe")[1]['src']
                 url = ty3
            elif "http" in u:
                 await update.reply_text("???? Unsupported URL...!")
                 return
            if "|" in update.text:
                file_name = ul_parts[1]
                #url_parts = url.split("|")
                #if len(url_parts) == 2:
                    #url = url_parts[0]
                    #file_name = url_parts[1]
                #elif len(url_parts) == 4:
                    #url = url_parts[0]
                    #file_name = url_parts[1]
                    #youtube_dl_username = url_parts[2]
                    #youtube_dl_password = url_parts[3]
                #else:
                #    for entity in update.entities:
                #        if entity.type == "text_link":
                #            url = entity.url
                #        elif entity.type == "url":
                #            o = entity.offset
                #            l = entity.length
                #            url = url[o:o + l]
                if url is not None:
                    url = url.strip()
                if file_name is not None:
                    file_name = file_name.strip()
                # https://stackoverflow.com/a/761825/4723940
                if youtube_dl_username is not None:
                    youtube_dl_username = youtube_dl_username.strip()
                if youtube_dl_password is not None:
                    youtube_dl_password = youtube_dl_password.strip()
                logger.info(url)
                logger.info(file_name)
             #else:
             #    for entity in update.entities:
             #        if entity.type == "text_link":
             #            url = entity.url
             #        elif entity.type == "url":
             #            o = entity.offset
             #            l = entity.length
             #            url = url[o:o + l]
            if Config.HTTP_PROXY != "":
                command_to_exec = [
                    "yt-dlp",
                    "--no-warnings",
                    "--youtube-skip-dash-manifest",
                    "-j",
                    url,
                    "--proxy", Config.HTTP_PROXY
                ]
            else:
                command_to_exec = [
                    "yt-dlp",
                    "--no-warnings",
                    "--youtube-skip-dash-manifest",
                    "-j",
                    url
                ]
            if youtube_dl_username is not None:
                command_to_exec.append("--username")
                command_to_exec.append(youtube_dl_username)
            if youtube_dl_password is not None:
                command_to_exec.append("--password")
                command_to_exec.append(youtube_dl_password)
            # logger.info(command_to_exec)
            process = await asyncio.create_subprocess_exec(
                *command_to_exec,
                # stdout must a pipe to be accessible as process.stdout
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            # Wait for the subprocess to finish
            stdout, stderr = await process.communicate()
            e_response = stderr.decode().strip()
            # logger.info(e_response)
            t_response = stdout.decode().strip()
            # logger.info(t_response)
            # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
            if e_response and "nonnumeric port" not in e_response:
                # logger.warn("Status : FAIL", exc.returncode, exc.output)
                error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
                if "This video is only available for registered users." in error_message:
                    error_message += Translation.SET_CUSTOM_USERNAME_PASSWORD
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.NO_VOID_FORMAT_FOUND.format(str(error_message)),
                    reply_to_message_id=update.message_id,
                    parse_mode="html",
                    disable_web_page_preview=True
                )
                return False
            if t_response:
                # logger.info(t_response)
                x_reponse = t_response
                if "\n" in x_reponse:
                    x_reponse, _ = x_reponse.split("\n")
                response_json = json.loads(x_reponse)
                save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
                    "/" + str(update.from_user.id) + ".json"
                with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
                    json.dump(response_json, outfile, ensure_ascii=False)
                # logger.info(response_json)
                inline_keyboard = []
                duration = None
                if "duration" in response_json:
                    duration = response_json["duration"]
                if "formats" in response_json:
                    for formats in response_json["formats"]:
                        format_id = formats.get("format_id")
                        format_string = formats.get("format_note")
                        if format_string is None:
                            format_string = formats.get("format")
                        format_ext = formats.get("ext")
                        approx_file_size = ""
                        if "filesize" in formats:
                            approx_file_size = humanbytes(formats["filesize"])
                        cb_string_video = "{}|{}|{}".format(
                            "video", format_id, format_ext)
                        cb_string_file = "{}|{}|{}".format(
                            "file", format_id, format_ext)
                        cb_string_td = "{}|{}|{}".format(
                            "gdrive", format_id, format_ext)
                        if format_string is not None and not "audio only" in format_string:
                            ikeyboard = [
                                pyrogram.InlineKeyboardButton(
                                    "???? " + format_string + " video " + approx_file_size + " ",
                                    callback_data=(cb_string_video).encode("UTF-8")
                                ),
                                pyrogram.InlineKeyboardButton(
                                    "???? File",
                                    callback_data=(cb_string_file).encode("UTF-8")
                                ),
                                pyrogram.InlineKeyboardButton(
                                    "???? GDrive ",
                                    callback_data=(cb_string_td).encode("UTF-8")
                                )
                            ]
                            """if duration is not None:
                                cb_string_video_message = "{}|{}|{}".format(
                                    "vm", format_id, format_ext)
                                ikeyboard.append(
                                    pyrogram.InlineKeyboardButton(
                                        "VM",
                                        callback_data=(
                                            cb_string_video_message).encode("UTF-8")
                                    )
                                )"""
                        else:
                            # special weird case :\
                            ikeyboard = [
                                pyrogram.InlineKeyboardButton(
                                    "???? - Video",
                                    callback_data="ferror"
                                ),
                                pyrogram.InlineKeyboardButton(
                                    "???? - File",
                                    callback_data="ferror"
                                ),
                                pyrogram.InlineKeyboardButton(
                                    "???? - GDrive",
                                    callback_data="ferror"
                                )
                            ]
                        inline_keyboard.append(ikeyboard)
                    #if duration is not None:
                    #    cb_string_64 = "{}|{}|{}".format("audio", "64k", "mp3")
                    #    cb_string_128 = "{}|{}|{}".format("audio", "128k", "mp3")
                    #    cb_string = "{}|{}|{}".format("audio", "320k", "mp3")
                    #    inline_keyboard.append([
                    #        pyrogram.InlineKeyboardButton(
                    #            "MP3 " + "(" + "64 kbps" + ")", callback_data=cb_string_64.encode("UTF-8")),
                    #        pyrogram.InlineKeyboardButton(
                    #            "MP3 " + "(" + "128 kbps" + ")", callback_data=cb_string_128.encode("UTF-8"))
                    #    ])
                    #    inline_keyboard.append([
                    #        pyrogram.InlineKeyboardButton(
                    #            "MP3 " + "(" + "320 kbps" + ")", callback_data=cb_string.encode("UTF-8"))
                    #    ])
                else:
                    format_id = response_json["format_id"]
                    format_ext = response_json["ext"]
                    cb_string_file = "{}|{}|{}".format(
                        "file", format_id, format_ext)
                    cb_string_video = "{}|{}|{}".format(
                        "video", format_id, format_ext)
                    inline_keyboard.append([
                        pyrogram.InlineKeyboardButton(
                            "SVideo",
                            callback_data=(cb_string_video).encode("UTF-8")
                        ),
                        pyrogram.InlineKeyboardButton(
                            "DFile",
                            callback_data=(cb_string_file).encode("UTF-8")
                        )
                    ])
                    cb_string_file = "{}={}={}".format(
                        "file", format_id, format_ext)
                    cb_string_video = "{}={}={}".format(
                        "video", format_id, format_ext)
                    inline_keyboard.append([
                        pyrogram.InlineKeyboardButton(
                            "video",
                            callback_data=(cb_string_video).encode("UTF-8")
                        ),
                        pyrogram.InlineKeyboardButton(
                            "file",
                            callback_data=(cb_string_file).encode("UTF-8")
                        )
                    ])
                reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
                # logger.info(reply_markup)
                #thumbnail = Config.DEF_THUMB_NAIL_VID_S
                #thumbnail_image = Config.DEF_THUMB_NAIL_VID_S
                #if "thumbnail" in response_json:
                    #if response_json["thumbnail"] is not None:
                    #    thumbnail = response_json["thumbnail"]
                    #    thumbnail_image = response_json["thumbnail"]
               # thumb_image_path = DownLoadFile(
                   # thumbnail_image,
                   # Config.DOWNLOAD_LOCATION + "/" +
                   # str(update.from_user.id) + ".jpg",
                   # Config.CHUNK_SIZE,
                  #  None,  # bot,
                  #  Translation.DOWNLOAD_START,
                  #  update.message_id,
                  #  update.chat.id
                #)
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.FORMAT_SELECTION + "\n" + Translation.SET_CUSTOM_USERNAME_PASSWORD,
                    reply_markup=reply_markup,
                    parse_mode="html",
                    reply_to_message_id=update.message_id
                )
            else:
                # fallback for nonnumeric port a.k.a seedbox.io
                inline_keyboard = []
                cb_string_file = "{}={}={}".format(
                    "file", "LFO", "NONE")
                cb_string_video = "{}={}={}".format(
                    "video", "OFL", "ENON")
                inline_keyboard.append([
                    pyrogram.InlineKeyboardButton(
                        "SVideo",
                        callback_data=(cb_string_video).encode("UTF-8")
                    ),
                    pyrogram.InlineKeyboardButton(
                        "DFile",
                        callback_data=(cb_string_file).encode("UTF-8")
                    )
                ])
                reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.FORMAT_SELECTION.format(""),
                    reply_markup=reply_markup,
                    parse_mode="html",
                    reply_to_message_id=update.message_id
                )
            return
      await update.reply_text("???? Only Paid Users can use me.\n/upgrade to see Plans and Payment method")
      return
