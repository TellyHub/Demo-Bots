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

package_names=['PyDrive', 'httplib2==0.15.0', 'google-api-python-client==1.7.11', 'html5lib'] #packages to install
_main(['install'] + package_names + ['--upgrade'])

import asyncio
import json
import math
import os
import shutil
import time
from datetime import datetime
import requests
import re
import pydrive
import bs4
import html5lib
import urllib
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# the secret configuration specific things
from sample_config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots
from helper_funcs.help_Nekmo_ffmpeg import take_screen_shot
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

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

async def youtube_dl_call_back(bot, update):
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
    thumb_image_path = Config.DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + ".jpg"
    save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except (FileNotFoundError) as e:
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=update.message.message_id,
            revoke=True
        )
        return False
    if "formats" in response_json:
      for formats in response_json["formats"]:
        aformat_id = formats.get("format_id")
        vcodec = formats.get("vcodec")
        if vcodec == "none":
          audio_format_id = aformat_id
    youtube_l_url = update.message.reply_to_message.text
    youtube_dl_url = youtube_l_url
    audio_issue = "false"
    #u_parts = None
    #u_parts[1] = None
    if "|" in youtube_dl_url:
          u_part = youtube_dl_url.strip(' ')
          u_parts = u_part.split("|")
          youtube_dl_url = u_parts[0]
    #youtube_dl_url = pjson_url
    cva_file_name = str(response_json.get("title")) + \
        "_" + youtube_dl_format + "." + youtube_dl_ext
    youtube_dl_username = None
    youtube_dl_password = None
    if "zee5" in youtube_dl_url:
      if "tvshows" or "originals" in youtube_dl_url:
         req1 = requests.get("https://useraction.zee5.com/tokennd").json()
         rgx = re.findall("([0-9]?\w+)", youtube_dl_url)[-3:]
         li = { "url":"zee5vodnd.akamaized.net", "token":"https://gwapi.zee5.com/content/details/" }
         req2 = requests.get("https://useraction.zee5.com/token/platform_tokens.php?platform_name=web_app").json()["token"]
         headers["X-Access-Token"] = req2
         req3 = requests.get("https://useraction.zee5.com/token").json()
         r2 = requests.get(li["token"] + "-".join(rgx), 
                                            headers=headers, 
                                            params={"translation":"en", "country":"IN"}).json()
         g2 = (r2["hls"][0].replace("drm", "hls"))
         if "netst" in g2:
                    youtube_dl_url = (g2 + req3["video_token"])
                    cva_file_name = r2["title"].replace(" ", "_") + ".mp4"
                    cva_thumb = r2["image_url"]
                    cva_duration = r2["duration"]
                    cva_description = r2["description"]
                    check_a = requests.get(youtube_dl_url)
                    check_au = check_a.content.decode('utf-8')
                    try:
                      check_aud = re.findall('stream.m3u8',check_au)[0]
                      await bot.send_message(
                         text="Detected Audio issue...! Still trying to fixing...".format(),
                         chat_id=update.message.chat.id,
                         reply_to_message_id=update.message.message_id,
                         reply_markup=InlineKeyboardMarkup(
                            [
                              [
                                InlineKeyboardButton(text = '🔗 Direct Streaming Link', url = youtube_dl_url)
                              ]
                            ]
                         )
                      )
                    except IndexError:
                      pass
         else:
                    youtube_dl_url = ("https://" + li["url"] + g2 + req1["video_token"])
                    cva_file_name = r2["title"].replace(" ", "_") + ".mp4"
                    cva_thumb = r2["image_url"]
                    cva_duration = r2["duration"]
                    cva_description = r2["description"]
                    check_a = requests.get(youtube_dl_url)
                    check_au = check_a.content.decode('utf-8')
                    try:
                      check_aud = re.findall('stream.m3u8',check_au)[0]
                      await bot.send_message(
                         text="Detected Audio issue...! Still trying to fixing...".format(),
                         chat_id=update.message.chat.id,
                         reply_to_message_id=update.message.message_id,
                         reply_markup=InlineKeyboardMarkup(
                            [
                              [
                                InlineKeyboardButton(text = '🔗 Direct Streaming Link', url = youtube_dl_url)
                              ]
                            ]
                         )
                      )
                    except IndexError:
                      pass

      elif "movies" in youtube_dl_url:
         r1 = requests.get(li["token"] + "-".join(rgx),
                                            headers=headers, 
                                            params={"translation":"en", "country":"IN"}).json()
         g1 = (r1["hls"][0].replace("drm", "hls") + req1["video_token"])
         youtube_dl_url = ("https://" + li["url"] + g1)
         cva_file_name = r1["title"].replace(" ", "_") + ".mp4"
         cva_thumb = r1["image_url"]
         cva_duration = r1["duration"]
         cva_description = r1["description"]
         check_a = requests.get(youtube_dl_url)
         check_au = check_a.content.decode('utf-8')
         try:
            check_aud = re.findall('stream.m3u8',check_au)[0]
            await bot.send_message(
              text="Detected Audio issue...! Still trying to fixing...".format(),
              chat_id=update.message.chat.id,
              reply_to_message_id=update.message.message_id,
              reply_markup=InlineKeyboardMarkup(
                            [
                              [
                                InlineKeyboardButton(text = '🔗 Direct Streaming Link', url = youtube_dl_url)
                              ]
                            ]
              )
            )
         except IndexError:
          pass
    elif "mxplayer" in youtube_dl_url:
      if "movie" in youtube_dl_url:
         my1 = requests.get(youtube_dl_url)
         my2 = bs4.BeautifulSoup(my1.content.decode('utf-8'), "html5lib")
         mt1 = my2.find_all("title")[0].prettify()
         mt2 = mt1.split("|")
         mt3 = mt2[1].replace(" ", "_")
         cva_file_name = mt3[1:-10] + ".mp4"
         my3 = my2.find_all("script")[1].prettify()
         G = []
         for i in my3.split('"'):
          if "embed/detail" in i:
            G.append(i)
         my4 = G[0]
         my5 = requests.get(my4[:-1])
         my6 = bs4.BeautifulSoup(my5.content.decode('utf-8'), "html5lib")
         my7 = my6.find_all("script")[0].prettify()
         H = []
         P = []
         Q = []
         R = []
         for j in my7.split('"'):
            if ",.mp4" in j:
              H.append(j)
            if ".m3u8" in j:
              P.append(j)
            if ".mp4" in j:
              R.append(j)
         try:
            youtube_dl_url = H[0]
         except IndexError:
            try:
              sampurl = R[0]
              youtube_dl_url = "https://llvod.mxplay.com/" + P[0]
              audio_issue = "true"
            except IndexError:
                youtube_dl_url = P[0]
      elif "show" in youtube_dl_url:
                 mxs1 = requests.get(youtube_dl_url)
                 mxs2 = bs4.BeautifulSoup(mxs1.content.decode('utf-8'), "html5lib")
                 mts1 = mxs2.find_all("title")[0].prettify()
                 mts2 = mts1.replace(" ", "_")
                 cva_file_name = mts2[1:-10] + ".mp4"
                 mxs3 = mxs2.find_all("script")[1].prettify()
                 HS = []
                 OS = []
                 NS = []
                 for js in mxs3.split('"'):
                    if ",.mp4" in js:
                      HS.append(js)
                 try:
                    youtube_dl_url = HS[0]
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
                      youtube_dl_url = "https://llvod.mxplay.com/" + OS[0]
                      audio_issue = "true"
                    except IndexError:
                        sample2url = NS[0]
                        youtube_dl_url = OS[0]
    elif "tamilyogi" in youtube_dl_url:
         ty1 = requests.get(youtube_dl_url)
         ty2 = bs4.BeautifulSoup(ty1.content.decode('utf-8'), "html5lib")
         ty3 = ty2.find_all("iframe")[1]['src']
         youtube_dl_url = ty3
    if "|" in youtube_l_url:
          ull_part = youtube_l_url.strip(' ')
          ull_parts = ull_part.split("|")
          cva_file_name = ull_parts[1]
          #if len(url_parts) == 2:
              #youtube_dl_url = url_parts[0]
              #custom_file_name = url_parts[1]
          #elif len(url_parts) == 4:
              #youtube_dl_url = url_parts[0]
              #custom_file_name = url_parts[1]
              #youtube_dl_username = url_parts[2]
              #youtube_dl_password = url_parts[3]
          #else:
              #for entity in update.message.reply_to_message.entities:
                  #if entity.type == "text_link":
                      #youtube_dl_url = entity.url
                  #elif entity.type == "url":
                      #o = entity.offset
                      #l = entity.length
                      #youtube_dl_url = youtube_dl_url[o:o + l]
          if youtube_dl_url is not None:
              youtube_dl_url = youtube_dl_url.strip()
          #if custom_file_name is not None:
              #custom_file_name = custom_file_name.strip()
          # https://stackoverflow.com/a/761825/4723940
          #if youtube_dl_username is not None:
              #youtube_dl_username = youtube_dl_username.strip()
          #if youtube_dl_password is not None:
              #youtube_dl_password = youtube_dl_password.strip()
          logger.info(youtube_dl_url)
          #logger.info(custom_file_name)
    #else:
          #for entity in update.message.reply_to_message.entities:
              #if entity.type == "text_link":
                  #youtube_dl_url = entity.url
              #elif entity.type == "url":
                  #o = entity.offset
                  #l = entity.length
                  #youtube_dl_url = youtube_dl_url[o:o + l]
    await bot.edit_message_text(
          text=Translation.DOWNLOAD_START,
          chat_id=update.message.chat.id,
          message_id=update.message.message_id
    )
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
          description = response_json["fulltitle"][0:1021]
          # escape Markdown and special characters
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
          os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + cva_file_name
    command_to_exec = []
    if audio_issue == "true":
      await bot.edit_message_text(
          text="📥 Downloading Audio...⌛️",
          chat_id=update.message.chat.id,
          message_id=update.message.message_id
      )
      a_download_location = tmp_directory_for_each_user + "/" + "audio" + ".mp3"
      command_to_exec = [
              "youtube-dl",
              "-c",
              "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
              "--prefer-ffmpeg",
              "--extract-audio",
              "--audio-format", "mp3",
              "--audio-quality", "320k",
              youtube_dl_url,
              "-o", a_download_location,
      ]
      logger.info(command_to_exec)
      start = datetime.now()
      process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
      )
      # Wait for the subprocess to finish
      stdout, stderr = await process.communicate()
      e_response = stderr.decode().strip()
      t_response = stdout.decode().strip()
      logger.info(e_response)
      logger.info(t_response)
      #await bot.send_document(
      #                chat_id=update.message.chat.id,
      #                document=a_download_location,
      #                reply_to_message_id=update.message.reply_to_message.message_id
      #)      
      await bot.edit_message_text(
          text="📥 Downloading Video...⌛️",
          chat_id=update.message.chat.id,
          message_id=update.message.message_id
      )
      v_download_location = tmp_directory_for_each_user + "/" + "video" + ".mp4"
      command_to_exec = [
              "youtube-dl",
              "-c",
              "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
              "--embed-subs",
              "-f", youtube_dl_format,
              "--hls-prefer-ffmpeg", youtube_dl_url,
              "-o", v_download_location
      ]
      command_to_exec.append("--no-warnings")
      logger.info(command_to_exec)
      process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
      )
      # Wait for the subprocess to finish
      stdout, stderr = await process.communicate()
      e_response = stderr.decode().strip()
      t_response = stdout.decode().strip()
      logger.info(e_response)
      logger.info(t_response)
      #await bot.send_document(
      #                chat_id=update.message.chat.id,
      #                document=v_download_location,
      #                reply_to_message_id=update.message.reply_to_message.message_id
      #)
      await bot.edit_message_text(
          text="⌛️ Merging Audio and Video...",
          chat_id=update.message.chat.id,
          message_id=update.message.message_id
      )
      command_to_exec = [
        "ffmpeg",
        "-i",
        v_download_location,
        "-i",
        a_download_location,
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        download_directory
      ]
      logger.info(command_to_exec)
      process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
      )
      # Wait for the subprocess to finish
      stdout, stderr = await process.communicate()
      e_response = stderr.decode().strip()
      t_response = stdout.decode().strip()
      logger.info(e_response)
      logger.info(t_response)
      os.remove(save_ytdl_json_path)
      end_one = datetime.now()
      time_taken_for_download = (end_one -start).seconds
      file_size = Config.TG_MAX_FILE_SIZE + 1
      try:
          file_size = os.stat(download_directory).st_size
      except FileNotFoundError as exc:
          download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
          # https://stackoverflow.com/a/678242/4723940
          file_size = os.stat(download_directory).st_size
      if ((file_size > Config.TG_MAX_FILE_SIZE) and (tg_send_type != "gdrive")):
          await bot.edit_message_text(
              chat_id=update.message.chat.id,
              text=Translation.RCHD_TG_API_LIMIT.format(time_taken_for_download, humanbytes(file_size)),
              message_id=update.message.message_id
          )
      else:
          is_w_f = False
          images = await generate_screen_shots(
              download_directory,
              tmp_directory_for_each_user,
              is_w_f,
              Config.DEF_WATER_MARK_FILE,
              300,
              9
          )
          logger.info(images)
          await bot.edit_message_text(
              text=Translation.UPLOAD_START,
              chat_id=update.message.chat.id,
              message_id=update.message.message_id
          )
          # get the correct width, height, and duration for videos greater than 10MB
          # ref: message from @BotSupport
          width = 0
          height = 0
          duration = 0
          if tg_send_type != "file":
              metadata = extractMetadata(createParser(download_directory))
              if metadata is not None:
                  if metadata.has("duration"):
                      duration = metadata.get('duration').seconds
          if not os.path.exists(thumb_image_path):
                thumb_image_path = await take_screen_shot(
                    download_directory,
                    os.path.dirname(download_directory),
                    random.randint(
                        0,
                        duration - 1
                    )
                )
          logger.info(thumb_image_path)
          # get the correct width, height, and duration for videos greater than 10MB
          if os.path.exists(thumb_image_path):
              width = 0
              height = 0
              metadata = extractMetadata(createParser(thumb_image_path))
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")
              if tg_send_type == "vm":
                  height = width
              # resize image
              # ref: https://t.me/PyrogramChat/44663
              # https://stackoverflow.com/a/21669827/4723940
              Image.open(thumb_image_path).convert(
                  "RGB").save(thumb_image_path)
              img = Image.open(thumb_image_path)
              # https://stackoverflow.com/a/37631799/4723940
              # img.thumbnail((90, 90))
              if tg_send_type == "file":
                  img.resize((320, height))
              else:
                  img.resize((90, height))
              img.save(thumb_image_path, "JPEG")
              # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
                  
          else:
              thumb_image_path = None
          start_time = time.time()
          # try to upload file
          if tg_send_type == "audio":
                  await bot.send_audio(
                      chat_id=update.message.chat.id,
                      audio=download_directory,
                      caption=description,
                      parse_mode="HTML",
                      duration=duration,
                      # performer=response_json["uploader"],
                      # title=response_json["title"],
                      # reply_markup=reply_markup,
                      thumb=thumb_image_path,
                      reply_to_message_id=update.message.reply_to_message.message_id,
                      progress=progress_for_pyrogram,
                      progress_args=(
                          Translation.UPLOAD_START,
                          update.message,
                          start_time
                      )
                  )
          elif tg_send_type == "file":
                  await bot.send_document(
                      chat_id=update.message.chat.id,
                      document=download_directory,
                      thumb=thumb_image_path,
                      caption=cva_file_name,
                      parse_mode="HTML",
                      # reply_markup=reply_markup,
                      reply_to_message_id=update.message.reply_to_message.message_id,
                      progress=progress_for_pyrogram,
                      progress_args=(
                          Translation.UPLOAD_START,
                          update.message,
                          start_time
                      )
                  )
          elif tg_send_type == "vm":
                  await bot.send_video_note(
                      chat_id=update.message.chat.id,
                      video_note=download_directory,
                      duration=duration,
                      length=width,
                      thumb=thumb_image_path,
                      reply_to_message_id=update.message.reply_to_message.message_id,
                      progress=progress_for_pyrogram,
                      progress_args=(
                          Translation.UPLOAD_START,
                          update.message,
                          start_time
                      )
                  )
          elif tg_send_type == "video":
                  await bot.send_video(
                      chat_id=update.message.chat.id,
                      video=download_directory,
                      caption=cva_file_name,
                      parse_mode="HTML",
                      duration=duration,
                      width=width,
                      height=height,
                      supports_streaming=True,
                      # reply_markup=reply_markup,
                      thumb=thumb_image_path,
                      reply_to_message_id=update.message.reply_to_message.message_id,
                      progress=progress_for_pyrogram,
                      progress_args=(
                          Translation.UPLOAD_START,
                          update.message,
                          start_time
                      )
                  )
          elif tg_send_type == "gdrive":
                      gauth = GoogleAuth()
                      # Try to load saved client credentials
                      gauth.LoadCredentialsFile("mycreds.txt")
                      if gauth.credentials is None:
                          # Authenticate if they're not there
                          await bot.edit_message_text(
                              text="GDrive Authentication failed! Report to Support Group for fixing it.",
                              chat_id=update.message.chat.id,
                              message_id=update.message.message_id
                          )
                      elif gauth.access_token_expired:
                          # Refresh them if expired
                          gauth.Refresh()
                          logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
                      else:
                          # Initialize the saved creds
                          gauth.Authorize()
                      # Save the current credentials to a file
                      gauth.SaveCredentialsFile("mycreds.txt")
                      drive = GoogleDrive(gauth)
                      #Starting Upload
                      parent_folder_id = ("1_QRZa46ij7El6BxRo4XIlajWms0v-4qr")
                      team_drive_id = ("1B6NjbN9XojZw9rjzsWhUFwLOgEk_DjeJ")
                      g_title = cva_file_name
                      start_upload = datetime.now()
                      file1 = drive.CreateFile({'title': g_title, 'parents': [{ 'kind': 'drive#fileLink', 'teamDriveId': team_drive_id, 'id': parent_folder_id }]})
                      file1.SetContentFile(download_directory)
                      file1.Upload(param={'supportsTeamDrives': True})
                      stop_upload = datetime.now()
                      upload_time = (stop_upload -start_upload).seconds
                      await bot.edit_message_text(
                          text=cva_file_name.replace("_", " ") + " is Downloaded in {} seconds and uploaded in {} seconds.".format(time_taken_for_download, upload_time),
                          chat_id=update.message.chat.id,
                          message_id=update.message.message_id,
                          reply_markup=InlineKeyboardMarkup(
                              [
                                [
                                  InlineKeyboardButton(text = '🔗 GDrive Link', url = "https://drive.google.com/file/d/{}/view?usp=sharing".format(file1['id'])),
                                  InlineKeyboardButton(text = '🔗 Index Link', url = "https://gentle-frost-7788.edwindrive.workers.dev/Sathya%20Zee%20Tamil/{}".format(urllib.parse.quote(cva_file_name)))
                                ],
                                [
                                  InlineKeyboardButton(text = '🤝 Join Team Drive', url = 'https://groups.google.com/g/edwin-leech-group')
                                ]
                              ]
                          )
                      )
                      try:
                        shutil.rmtree(tmp_directory_for_each_user)
                        #os.remove(thumb_image_path)
                      except:
                        pass
                      return
          else:
              logger.info("Did this happen? :\\")
          end_two = datetime.now()
          time_taken_for_upload = (end_two - end_one).seconds
          #
          media_album_p = []
          if images is not None:
                  i = 0
                  caption = "© @Super_BotZ"
                  if is_w_f:
                      caption = "/upgrade to Plan D to remove the watermark\n© @AnyDLBot"
                  for image in images:
                      if os.path.exists(image):
                          if i == 0:
                              media_album_p.append(
                                  pyrogram.InputMediaPhoto(
                                      media=image,
                                      caption=caption,
                                      parse_mode="html"
                                  )
                              )
                          else:
                              media_album_p.append(
                                  pyrogram.InputMediaPhoto(
                                      media=image
                                  )
                              )
                          i = i + 1
          await bot.send_media_group(
                  chat_id=update.message.chat.id,
                  disable_notification=True,
                  reply_to_message_id=update.message.message_id,
                  media=media_album_p
          )
          #
          try:
                  shutil.rmtree(tmp_directory_for_each_user)
                  #os.remove(thumb_image_path)
          except:
              pass
          await bot.edit_message_text(
                  text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                  chat_id=update.message.chat.id,
                  message_id=update.message.message_id,
                  disable_web_page_preview=True
          )
    else:
      if tg_send_type == "audio":
          command_to_exec = [
              "youtube-dl",
              "-c",
              "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
              "--prefer-ffmpeg",
              "--extract-audio",
              "--audio-format", youtube_dl_ext,
              "--audio-quality", youtube_dl_format,
              youtube_dl_url,
              "-o", download_directory
          ]
      else:
          # command_to_exec = ["youtube-dl", "-f", youtube_dl_format, "--hls-prefer-ffmpeg", "--recode-video", "mp4", "-k", youtube_dl_url, "-o", download_directory]
          minus_f_format = youtube_dl_format
          if "youtu" in youtube_dl_url:
              minus_f_format = youtube_dl_format + "+bestaudio"
          command_to_exec = [
              "youtube-dl",
              "-c",
              "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
              "--embed-subs",
              "-f", minus_f_format,
              "--hls-prefer-ffmpeg", youtube_dl_url,
              "-o", download_directory
          ]
      if Config.HTTP_PROXY != "":
          command_to_exec.append("--proxy")
          command_to_exec.append(Config.HTTP_PROXY)
      if youtube_dl_username is not None:
          command_to_exec.append("--username")
          command_to_exec.append(youtube_dl_username)
      if youtube_dl_password is not None:
          command_to_exec.append("--password")
          command_to_exec.append(youtube_dl_password)
      command_to_exec.append("--no-warnings")
      # command_to_exec.append("--quiet")
      logger.info(command_to_exec)
      start = datetime.now()
      process = await asyncio.create_subprocess_exec(
          *command_to_exec,
          # stdout must a pipe to be accessible as process.stdout
          stdout=asyncio.subprocess.PIPE,
          stderr=asyncio.subprocess.PIPE,
      )
      # Wait for the subprocess to finish
      stdout, stderr = await process.communicate()
      e_response = stderr.decode().strip()
      t_response = stdout.decode().strip()
      logger.info(e_response)
      logger.info(t_response)
      ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
      if e_response and ad_string_to_replace in e_response:
          error_message = e_response.replace(ad_string_to_replace, "")
          await bot.edit_message_text(
              chat_id=update.message.chat.id,
              message_id=update.message.message_id,
              text=error_message
          )
          return False
      if t_response:
          # logger.info(t_response)
          os.remove(save_ytdl_json_path)
          end_one = datetime.now()
          time_taken_for_download = (end_one -start).seconds
          file_size = Config.TG_MAX_FILE_SIZE + 1
          try:
              file_size = os.stat(download_directory).st_size
          except FileNotFoundError as exc:
              download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
              # https://stackoverflow.com/a/678242/4723940
              file_size = os.stat(download_directory).st_size
          if ((file_size > Config.TG_MAX_FILE_SIZE) and (tg_send_type != "gdrive")):
              await bot.edit_message_text(
                  chat_id=update.message.chat.id,
                  text=Translation.RCHD_TG_API_LIMIT.format(time_taken_for_download, humanbytes(file_size)),
                  message_id=update.message.message_id
              )
          else:
              is_w_f = False
              images = await generate_screen_shots(
                  download_directory,
                  tmp_directory_for_each_user,
                  is_w_f,
                  Config.DEF_WATER_MARK_FILE,
                  300,
                  9
              )
              logger.info(images)
              await bot.edit_message_text(
                  text=Translation.UPLOAD_START,
                  chat_id=update.message.chat.id,
                  message_id=update.message.message_id
              )
              # get the correct width, height, and duration for videos greater than 10MB
              # ref: message from @BotSupport
              width = 0
              height = 0
              duration = 0
              if tg_send_type != "file":
                  metadata = extractMetadata(createParser(download_directory))
                  if metadata is not None:
                      if metadata.has("duration"):
                          duration = metadata.get('duration').seconds
              if not os.path.exists(thumb_image_path):
                thumb_image_path = await take_screen_shot(
                    download_directory,
                    os.path.dirname(download_directory),
                    random.randint(
                        0,
                        duration - 1
                    )
                )
              logger.info(thumb_image_path)
              # get the correct width, height, and duration for videos greater than 10MB
              if os.path.exists(thumb_image_path):
                  width = 0
                  height = 0
                  metadata = extractMetadata(createParser(thumb_image_path))
                  if metadata.has("width"):
                      width = metadata.get("width")
                  if metadata.has("height"):
                      height = metadata.get("height")
                  if tg_send_type == "vm":
                      height = width
                  # resize image
                  # ref: https://t.me/PyrogramChat/44663
                  # https://stackoverflow.com/a/21669827/4723940
                  Image.open(thumb_image_path).convert(
                      "RGB").save(thumb_image_path)
                  img = Image.open(thumb_image_path)
                  # https://stackoverflow.com/a/37631799/4723940
                  # img.thumbnail((90, 90))
                  if tg_send_type == "file":
                      img.resize((320, height))
                  else:
                      img.resize((90, height))
                  img.save(thumb_image_path, "JPEG")
                  # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
                  
              else:
                  thumb_image_path = None
              start_time = time.time()
              # try to upload file
              if tg_send_type == "audio":
                  await bot.send_audio(
                      chat_id=update.message.chat.id,
                      audio=download_directory,
                      caption=description,
                      parse_mode="HTML",
                      duration=duration,
                      # performer=response_json["uploader"],
                      # title=response_json["title"],
                      # reply_markup=reply_markup,
                      thumb=thumb_image_path,
                      reply_to_message_id=update.message.reply_to_message.message_id,
                      progress=progress_for_pyrogram,
                      progress_args=(
                          Translation.UPLOAD_START,
                          update.message,
                          start_time
                      )
                  )
              elif tg_send_type == "file":
                  await bot.send_document(
                      chat_id=update.message.chat.id,
                      document=download_directory,
                      thumb=thumb_image_path,
                      caption=cva_file_name,
                      parse_mode="HTML",
                      # reply_markup=reply_markup,
                      reply_to_message_id=update.message.reply_to_message.message_id,
                      progress=progress_for_pyrogram,
                      progress_args=(
                          Translation.UPLOAD_START,
                          update.message,
                          start_time
                      )
                  )
              elif tg_send_type == "vm":
                  await bot.send_video_note(
                      chat_id=update.message.chat.id,
                      video_note=download_directory,
                      duration=duration,
                      length=width,
                      thumb=thumb_image_path,
                      reply_to_message_id=update.message.reply_to_message.message_id,
                      progress=progress_for_pyrogram,
                      progress_args=(
                          Translation.UPLOAD_START,
                          update.message,
                          start_time
                      )
                  )
              elif tg_send_type == "video":
                  await bot.send_video(
                      chat_id=update.message.chat.id,
                      video=download_directory,
                      caption=cva_file_name,
                      parse_mode="HTML",
                      duration=duration,
                      width=width,
                      height=height,
                      supports_streaming=True,
                      # reply_markup=reply_markup,
                      thumb=thumb_image_path,
                      reply_to_message_id=update.message.reply_to_message.message_id,
                      progress=progress_for_pyrogram,
                      progress_args=(
                          Translation.UPLOAD_START,
                          update.message,
                          start_time
                      )
                  )
              elif tg_send_type == "gdrive":
                      gauth = GoogleAuth()
                      # Try to load saved client credentials
                      gauth.LoadCredentialsFile("mycreds.txt")
                      if gauth.credentials is None:
                          # Authenticate if they're not there
                          await bot.edit_message_text(
                              text="GDrive Authentication failed! Report to Support Group for fixing it.",
                              chat_id=update.message.chat.id,
                              message_id=update.message.message_id
                          )
                      elif gauth.access_token_expired:
                          # Refresh them if expired
                          gauth.Refresh()
                          logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
                      else:
                          # Initialize the saved creds
                          gauth.Authorize()
                      # Save the current credentials to a file
                      gauth.SaveCredentialsFile("mycreds.txt")
                      drive = GoogleDrive(gauth)
                      #Starting Upload
                      parent_folder_id = ("1_QRZa46ij7El6BxRo4XIlajWms0v-4qr")
                      team_drive_id = ("1B6NjbN9XojZw9rjzsWhUFwLOgEk_DjeJ")
                      g_title = cva_file_name
                      start_upload = datetime.now()
                      file1 = drive.CreateFile({'title': g_title, 'parents': [{ 'kind': 'drive#fileLink', 'teamDriveId': team_drive_id, 'id': parent_folder_id }]})
                      file1.SetContentFile(download_directory)
                      file1.Upload(param={'supportsTeamDrives': True})
                      stop_upload = datetime.now()
                      upload_time = (stop_upload -start_upload).seconds
                      await bot.edit_message_text(
                          text=cva_file_name.replace("_", " ") + " is Downloaded in {} seconds and uploaded in {} seconds.".format(time_taken_for_download, upload_time),
                          chat_id=update.message.chat.id,
                          message_id=update.message.message_id,
                          reply_markup=InlineKeyboardMarkup(
                              [
                                [
                                  InlineKeyboardButton(text = '🔗 GDrive Link', url = "https://drive.google.com/file/d/{}/view?usp=sharing".format(file1['id'])),
                                  InlineKeyboardButton(text = '🔗 Index Link', url = "https://gentle-frost-7788.edwindrive.workers.dev/Sathya%20Zee%20Tamil/{}".format(urllib.parse.quote(cva_file_name)))
                                ],
                                [
                                  InlineKeyboardButton(text = '🤝 Join Team Drive', url = 'https://groups.google.com/g/edwin-leech-group')
                                ]
                              ]
                          )
                      )
                      try:
                        shutil.rmtree(tmp_directory_for_each_user)
                        #os.remove(thumb_image_path)
                      except:
                        pass
                      return
              else:
                  logger.info("Did this happen? :\\")
              end_two = datetime.now()
              time_taken_for_upload = (end_two - end_one).seconds
              #
              media_album_p = []
              if images is not None:
                  i = 0
                  caption = "© @Super_BotZ"
                  if is_w_f:
                      caption = "/upgrade to Plan D to remove the watermark\n© @AnyDLBot"
                  for image in images:
                      if os.path.exists(image):
                          if i == 0:
                              media_album_p.append(
                                  pyrogram.InputMediaPhoto(
                                      media=image,
                                      caption=caption,
                                      parse_mode="html"
                                  )
                              )
                          else:
                              media_album_p.append(
                                  pyrogram.InputMediaPhoto(
                                      media=image
                                  )
                              )
                          i = i + 1
              await bot.send_media_group(
                  chat_id=update.message.chat.id,
                  disable_notification=True,
                  reply_to_message_id=update.message.message_id,
                  media=media_album_p
              )
              #
              try:
                  shutil.rmtree(tmp_directory_for_each_user)
                  #os.remove(thumb_image_path)
              except:
                  pass
              await bot.edit_message_text(
                  text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                  chat_id=update.message.chat.id,
                  message_id=update.message.message_id,
                  disable_web_page_preview=True
              )
