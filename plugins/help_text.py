#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import sqlite3
import shutil
import time
import json
from datetime import datetime, timedelta

# the secret configuration specific things
from sample_config import Config

# the Strings used for this "thing"
from translation import Translation
from helper_funcs.display_progress import humanbytes, TimeFormatter
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup


async def help_user(bot, update):
    await bot.send_message(
        chat_id=update.from_user.id,
        text=Translation.HELP_USER,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message.message_id,
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(text = '💬 Support Group ', url="https://t.me/Super_botz_support"),
                    InlineKeyboardButton(text = '✅ Updates Channel', url = "https://t.me/Super_botz")
                ],
                [
                    InlineKeyboardButton(text = '✍🏼 Custom File Name ', url="https://www.youtube.com/watch?v=5wSi4KC70Gw&t=2m5s")
                 
                ],
                [
                     InlineKeyboardButton(text = '🏞 Custom Thumbnail', url = "https://www.youtube.com/watch?v=5wSi4KC70Gw&t=3m33s")
                ],
                [
                    InlineKeyboardButton(text = '📽️ Tutorial', url = "https://youtu.be/5wSi4KC70Gw"),
                    InlineKeyboardButton(text = '🔐 Close ', callback_data="close")
                ]
            ]
        )
    )

@pyrogram.Client.on_message(pyrogram.Filters.command(["start"]))
async def start(bot, update):
    with open("backup.json", "r", encoding="utf8") as f:
            b_json = json.load(f)
    for users in b_json["users"]:
          user = users.get("user_id")
          plan = users.get("plan_name")
          exp = users.get("expire_on")
          if int(update.chat.id) == int(user):
            await bot.send_message(
                chat_id=update.chat.id,
                text=Translation.START_TEXT,
                reply_to_message_id=update.message_id,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [ 
                        [
                            InlineKeyboardButton(text = 'ℹ️ Help ', callback_data="help_back"),
                            InlineKeyboardButton(text = '🔐 Close ', callback_data="close")
                        ],
                        [
                            InlineKeyboardButton(text = '💬 Helpline', url="https://t.me/Super_botz_support")
                        ]
                    ]
                )
            )
            return
    await update.reply_text("🤑 Only Paid Users can use me.\n/upgrade to see Plans and Payment method")
    return

@pyrogram.Client.on_message(pyrogram.Filters.command(["bugs"]))
async def bugs(bot, update):
    with open("backup.json", "r", encoding="utf8") as f:
            b_json = json.load(f)
    for users in b_json["users"]:
          user = users.get("user_id")
          plan = users.get("plan_name")
          exp = users.get("expire_on")
          if int(update.chat.id) == int(user):
            await bot.send_message(
                chat_id=update.chat.id,
                text=Translation.TODO,
                reply_to_message_id=update.message_id
            )
            return
    else:
      await update.reply_text("🤑 Only Paid Users can use me.\n/upgrade to see Plans and Payment method")
      return



@pyrogram.Client.on_message(pyrogram.Filters.command(["upgrade"]))
async def upgrade(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UPGRADE_TEXT,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text = '📽️ Proof', url = "https://youtu.be/5wSi4KC70Gw"),
                    InlineKeyboardButton(text = '🔐 Close ', callback_data="close")
                ],
                [
                     InlineKeyboardButton(text = '🤩 How to get for Free?', callback_data = "free_req")
                ]
            ]
        )
    )

#@pyrogram.Client.on_message(pyrogram.Filters.command(["free"]))
async def free_req(bot, update):
    await bot.send_message(
        chat_id=update.from_user.id,
        text=Translation.REQ_FREE_TEXT,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message.message_id,
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(text = '🤩 YouTube Channel ', url="https://youtube.com/c/cvatricks"),
                    InlineKeyboardButton(text = '🔐 Close ', callback_data="close")
                ]
            ]
        )
    )
@pyrogram.Client.on_message(pyrogram.Filters.command(["status"]))
async def status_message_f(client, message):
    currentTime = time.strftime("%H:%M:%S", time.gmtime(time.time() - Config.BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)

    ms_g = f"<b><u>Server Status:</u></b>\n\n" \
        f"<b>🕒 Bot Uptime</b>: <code>{currentTime}</code>\n\n" \
        f"<b>🗄 Total disk space</b>: <code>{total}</code>\n\n" \
        f"<b>🗄 Used</b>: <code>{used}</code>\n\n" \
        f"<b>🗄 Free</b>: <code>{free}</code>\n\n"
    buttons = [[
        InlineKeyboardButton('🔄 Refresh', callback_data="rfrsh"),
        InlineKeyboardButton('🔐 Close', callback_data="close")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    msg = ms_g
    await message.reply_text(msg, reply_markup=reply_markup, quote=True)

async def rfrsh(client, message):
    currentTime = time.strftime("%H:%M:%S", time.gmtime(time.time() - Config.BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)

    ms_g = f"<b><u>Server Status:</u></b>\n\n" \
        f"<b>🕒 Bot Uptime</b>: <code>{currentTime}</code>\n\n" \
        f"<b>🗄 Total disk space</b>: <code>{total}</code>\n\n" \
        f"<b>🗄 Used</b>: <code>{used}</code>\n\n" \
        f"<b>🗄 Free</b>: <code>{free}</code>\n\n"
    buttons = [[
        InlineKeyboardButton('🔄 Refresh', callback_data="rfrsh"),
        InlineKeyboardButton('🔐 Close', callback_data="close")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    msg = ms_g
    await message.edit_message_text(msg, reply_markup=reply_markup)

async def errorformat(bot, update):
  await bot.answer_callback_query(
    update.id,
    text="Invalid Format...!",
    show_alert=True
  )

@pyrogram.Client.on_message(pyrogram.Filters.command(["backup"]))
async def backup(bot, update):
 if update.from_user.id == 695291232:
   b_file = "backup.json"
   await bot.send_document(
       chat_id=update.from_user.id,
       document=b_file
   )
 else:
   await update.reply_text("You are not Owner...!")

@pyrogram.Client.on_message(pyrogram.Filters.command(["add"]))
async def add(bot, update):
 if update.from_user.id == 695291232:
   new_u = update.text
   new_us = new_u.split(' ')
   if len(new_us) == 4:
     new_user = new_us[1]
     act_plan = new_us[2]
     d = new_us[3]
     paid_date = datetime.now()
     expiry_date = paid_date + timedelta(days=int(d))
     with open("backup.json", "r", encoding="utf8") as f:
              b_json = json.load(f)
     b_json["users"].append({
        "user_id": "{}".format(new_user),
        "plan_name": "{}".format(act_plan),
        "paid_on": "{}".format(paid_date),
        "expire_on": '{}'.format(expiry_date)
     })
     with open("backup.json", "w", encoding="utf8") as outfile:
              json.dump(b_json, outfile, ensure_ascii=False)
     await update.reply_text("✅ User ID {} is added and Expire on {}th {} {}".format(new_user,expiry_date.strftime("%d"),expiry_date.strftime("%B"),expiry_date.strftime("%Y")))
   else:
     await update.reply_text("Eg.: /add 123456 Trial 1")
 else:
   await update.reply_text("You are not Owner...!")

@pyrogram.Client.on_message(pyrogram.Filters.command(["restore"]))
async def restore(bot, update):
 if update.from_user.id == 695291232:
   if update.reply_to_message is not None:
      the_real_download_location = [
        {"user_id": "695291232", "plan_name": "Owner", "paid_on": "2020-10-20 10:20:02.657517", "expire_on": "2022-10-21 10:20:02.657517"},
        {"user_id": "347246166", "plan_name": "Paid 1", "paid_on": "2020-10-21 17:22:02.657517", "expire_on": "2020-11-19 17:22:02.657517"},
        {"user_id": "825450340", "plan_name": "Paid 1", "paid_on": "2020-10-21 12:50:02.657517", "expire_on": "2020-11-19 12:50:02.657517"},
        {"user_id": "541492257", "plan_name": "Paid 1", "paid_on": "2020-10-19 12:50:02.657517", "expire_on": "2020-11-17 12:50:02.657517"},
        {"user_id": "946913552", "plan_name": "Paid 1", "paid_on": "2020-10-13 21:50:02.657517", "expire_on": "2020-11-12 21:50:02.657517"},
        {"user_id": "1366337468", "plan_name": "Paid 1", "paid_on": "2020-10-06 20:50:02.657517", "expire_on": "2020-11-05 20:50:02.657517"},
        {"user_id": "680843492", "plan_name": "Paid 1", "paid_on": "2020-10-03 20:50:02.657517", "expire_on": "2020-11-02 20:50:02.657517"},
        {"user_id": "1270348754", "plan_name": "Paid 1", "paid_on": "2020-09-29 20:50:02.657517", "expire_on": "2020-10-29 20:50:02.657517"},
        {"user_id": "1080989904", "plan_name": "Paid 1", "paid_on": "2020-09-29 20:50:02.657517", "expire_on": "2020-10-29 20:50:02.657517"},
        {"user_id": "917099183", "plan_name": "Paid 1", "paid_on": "2020-09-15 20:50:02.657517", "expire_on": "2020-10-24 20:50:02.657517"},
        {"user_id": "698900540", "plan_name": "Paid2", "paid_on": "2020-10-25 17:42:12.126426", "expire_on": "2020-11-24 17:42:12.126426"},
        {"user_id": "699615803", "plan_name": "X_row", "paid_on": "2020-10-26 03:30:32.945845", "expire_on": "2020-11-25 03:30:32.945845"},
        {"user_id": "919584113", "plan_name": "SBBotOwner", "paid_on": "2020-10-26 03:31:18.875428", "expire_on": "2020-11-25 03:31:18.875428"},
        {"user_id": "923064952", "plan_name": "paid2", "paid_on": "2020-10-26 04:54:14.276850", "expire_on": "2020-12-23 04:54:14.276850"},
        {"user_id": "683538773", "plan_name": "Viruzz_Dev", "paid_on": "2020-10-26 05:19:42.963176", "expire_on": "2020-11-25 05:19:42.963176"},
        {"user_id": "1153786300", "plan_name": "UKNum_Owner", "paid_on": "2020-10-26 07:34:21.067216", "expire_on": "2020-11-25 07:34:21.067216"},
        {"user_id": "568715538", "plan_name": "Paid1", "paid_on": "2020-10-26 09:33:17.084030", "expire_on": "2020-11-25 09:33:17.084030"},
        {"user_id": "1366337468", "plan_name": "Paid2", "paid_on": "2020-10-28 04:47:12.065712", "expire_on": "2020-12-05 04:47:12.065712"},
        {"user_id": "751444330", "plan_name": "Paid1", "paid_on": "2020-10-28 08:35:04.028298", "expire_on": "2020-11-27 08:35:04.028298"},
        {"user_id": "652767901", "plan_name": "Paid1", "paid_on": "2020-10-28 22:41:20.631243", "expire_on": "2020-11-27 22:41:20.631243"},
        {"user_id": "1193583027", "plan_name": "Paid1", "paid_on": "2020-10-30 10:55:34.673150", "expire_on": "2020-11-29 10:55:34.673150"},
        {"user_id": "1304514243", "plan_name": "Paid1", "paid_on": "2020-10-30 11:19:44.657497", "expire_on": "2020-11-29 11:19:44.657497"},
        {"user_id": "978417324", "plan_name": "Trial", "paid_on": "2020-10-30 14:39:20.385529", "expire_on": "2020-10-31 14:39:20.385529"},
        {"user_id": "1036705995", "plan_name": "Paid1", "paid_on": "2020-11-02 02:58:16.037052", "expire_on": "2020-12-02 02:58:16.037052"},
        {"user_id": "983851680", "plan_name": "Paid2", "paid_on": "2020-11-10 05:06:43.454024", "expire_on": "2020-12-10 05:06:43.454024"},
        {"user_id": "685160004", "plan_name": "Paid1", "paid_on": "2020-11-12 10:16:46.162865", "expire_on": "2020-12-12 10:16:46.162865"},
        {"user_id": "1100005332", "plan_name": "Paid1", "paid_on": "2020-11-15 04:53:29.039063", "expire_on": "2020-12-15 04:53:29.039063"},
        {"user_id": "1080989904", "plan_name": "Paid2", "paid_on": "2020-11-16 14:34:35.523843", "expire_on": "2020-12-16 14:34:35.523843"}
      ]
      x = Config.BOTDB.insert_many(the_real_download_location)
      await update.reply_text("✅ Backup file sucessfully restored.")
   else:
     await update.reply_text("Please reply to backup file...!")
 else:
   await update.reply_text("You are not Owner...!")


@pyrogram.Client.on_message(pyrogram.Filters.command(["me"]))
async def me(bot, update):
    #with open("backup.json", "r", encoding="utf8") as f:
    #        b_json = json.load(f)
    for users in Config.BOTDB:
          user = users.get("user_id")
          plan = users.get("plan_name")
          exp = users.get("expire_on")
          if int(update.chat.id) == int(user):
            await bot.send_message(
              chat_id=update.chat.id,
              text=Translation.CURENT_PLAN_DETAILS.format(user, plan, datetime.strptime(exp, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')),
              parse_mode="html",
              disable_web_page_preview=True,
              reply_to_message_id=update.message_id
            )
            return
    await update.reply_text("🤑 Only Paid Users can use me.\n/upgrade to see Plans and Payment method")

@pyrogram.Client.on_message(pyrogram.Filters.command(["resetsession"]))
async def resetsession(bot, update):
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    thumb_image_path = Config.DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + ".jpg"
    if update.from_user.id in Config.ONE_BY_ONE:
        Config.ONE_BY_ONE.remove(update.from_user.id)
    #if os.path.exists(thumb_image_path):
        #shutil.rmtree(thumb_image_path)
    if os.path.exists(tmp_directory_for_each_user):
        shutil.rmtree(tmp_directory_for_each_user)
    await update.reply_text("✅ Session Restarted successfully.")
