#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import json
import math
import os
import shutil
import subprocess
import time

from sample_config import Config
# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.help_text import help_user
from plugins.help_text import free_req
from plugins.help_text import rfrsh
from plugins.dl_button import ddl_call_back
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image


@pyrogram.Client.on_callback_query()
async def button(bot, update):
    # logger.info(update)
    cb_data = update.data

    if "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    elif "=" in cb_data:
        await ddl_call_back(bot, update)
    elif "help_back" in cb_data:
        await update.message.delete()
        await help_user(bot, update)
    elif "close" in cb_data:
        await update.message.delete()
    elif "free_req" in cb_data:
        await update.message.delete()
        await free_req(bot, update)
    elif "rfrsh" in cb_data:
        #await update.message.delete()
        await rfrsh(bot, update)
