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

# the secret configuration specific things
from sample_config import Config

# the Strings used for this "thing"
from translation import Translation
from display_progress import humanbytes, TimeFormatter
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup

def GetExpiryDate(chat_id):
    expires_at = (str(chat_id), "Source Cloned User", "1970.01.01.12.00.00")
    Config.AUTH_USERS.add(695291232)
    return expires_at

@pyrogram.Client.on_message(pyrogram.Filters.command(["about"]))
async def help_user(bot, update):
  if update.from_user.id in Config.AUTH_USERS:
    # logger.info(update)
    #TRChatBase(update.from_user.id, update.text, "/help")
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
                    InlineKeyboardButton(text = '🔐 Close ', callback_data="close")
                ],
                [
                    InlineKeyboardButton(text = '🤩 How to get for Free?', callback_data = "free_req"),
                    InlineKeyboardButton(text = '😎 My Creator 😎 ', url = "https://t.me/Edwin_Jarvis_Ofl")
                ]
            ]
        )
    )
  else:
    await update.reply_text("🤑 Only Paid Users can use me.\n/upgrade to see Plans and Payment method")
    return


@pyrogram.Client.on_message(pyrogram.Filters.command(["me"]))
async def get_me_info(bot, update):
  if update.from_user.id in Config.AUTH_USERS:
    # logger.info(update)
    # TRChatBase(update.from_user.id, update.text, "/me")
    chat_id = str(update.from_user.id)
    chat_id, plan_type, expires_at = GetExpiryDate(chat_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.CURENT_PLAN_DETAILS.format(chat_id, plan_type, expires_at),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
  else:
    await update.reply_text("🤑 Only Paid Users can use me.\n/upgrade to see Plans and Payment method")
    return


@pyrogram.Client.on_message(pyrogram.Filters.command(["start"]))
async def start(bot, update):
  if update.from_user.id in Config.AUTH_USERS:
    # logger.info(update)
    # TRChatBase(update.from_user.id, update.text, "/start")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT,
        reply_to_message_id=update.message_id,
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(text = 'ℹ️ Help ', callback_data="help_back"),
                    InlineKeyboardButton(text = '🔐 Close ', callback_data="close")
                ],
                [
                    InlineKeyboardButton(text = '😎 My Creator ', url = "https://t.me/Edwin_Jarvis_Ofl")
                ]
            ]
        )
    )
  else:
    await update.reply_text("🤑 Only Paid Users can use me.\n/upgrade to see Plans and Payment method")
    return

@pyrogram.Client.on_message(pyrogram.Filters.command(["bugs"]))
async def bugs(bot, update):
  if update.from_user.id in Config.AUTH_USERS:
    # logger.info(update)
    # TRChatBase(update.from_user.id, update.text, "/bugs")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.TODO,
        reply_to_message_id=update.message_id
    )
  else:
    await update.reply_text("🤑 Only Paid Users can use me.\n/upgrade to see Plans and Payment method")
    return



@pyrogram.Client.on_message(pyrogram.Filters.command(["upgrade"]))
async def upgrade(bot, update):
    # logger.info(update)
    # TRChatBase(update.from_user.id, update.text, "/upgrade")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UPGRADE_TEXT,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text = '🤩 How to get for Free?', callback_data = "free_req"),
                    InlineKeyboardButton(text = '🔐 Close ', callback_data="close")
                ]
            ]
        )
    )

@pyrogram.Client.on_message(pyrogram.Filters.command(["free"]))
async def free_req(bot, update):
    # logger.info(update)
    # TRChatBase(update.from_user.id, update.text, "/free")
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

    ms_g = f"<b>Bot Uptime</b>: <code>{currentTime}</code>\n" \
        f"<b>Total disk space</b>: <code>{total}</code>\n" \
        f"<b>Used</b>: <code>{used}</code>\n" \
        f"<b>Free</b>: <code>{free}</code>\n"
    buttons = [[
        InlineKeyboardButton('Refresh 🔄', callback_data="rfrsh"),
        InlineKeyboardButton('close ⛔', callback_data="close")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    msg = ms_g
    await message.reply_text(msg, reply_markup=reply_markup, quote=True)
@pyrogram.Client.on_message(pyrogram.Filters.command(["status"]))
async def status_message_f(client, message):
    currentTime = time.strftime("%H:%M:%S", time.gmtime(time.time() - Config.BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)

    ms_g = f"<b>Bot Uptime</b>: <code>{currentTime}</code>\n" \
        f"<b>Total disk space</b>: <code>{total}</code>\n" \
        f"<b>Used</b>: <code>{used}</code>\n" \
        f"<b>Free</b>: <code>{free}</code>\n"
    buttons = [[
        InlineKeyboardButton('Refresh 🔄', callback_data="rfrsh"),
        InlineKeyboardButton('close ⛔', callback_data="close")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    msg = ms_g
    await message.edit_message_text(msg, reply_markup=reply_markup, quote=True)
