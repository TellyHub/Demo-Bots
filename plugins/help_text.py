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
from bson import json_util
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
    await bot.edit_message_text(
        chat_id=update.message.from_user.id,
        message_id=update.message.message_id,
        text=Translation.HELP_USER,
        parse_mode="html",
        disable_web_page_preview=True,
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
    for users in Config.BOTDB.find():
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
    for users in Config.BOTDB.find():
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
    await bot.edit_message_text(
        chat_id=update.message.from_user.id,
        message_id=update.message.message_id,
        text=Translation.REQ_FREE_TEXT,
        parse_mode="html",
        disable_web_page_preview=True,
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


@pyrogram.Client.on_message(pyrogram.Filters.command(["me"]))
async def me(bot, update):
    for users in Config.BOTDB.find():
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
    if os.path.exists(thumb_image_path):
        shutil.rmtree(thumb_image_path)
    if os.path.exists(tmp_directory_for_each_user):
        shutil.rmtree(tmp_directory_for_each_user)
    await update.reply_text("✅ Session Restarted successfully.")
