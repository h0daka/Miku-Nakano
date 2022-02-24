import time
import importlib
from sys import argv
import re
import os
import asyncio
from typing import List
from MikuXProBot.modules.sudoers import bot_sys_stats

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    run_async,
    MessageHandler,
)

from MikuXProBot import StartTime, dispatcher, pgram
from pyrogram import filters
from MikuXProBot.modules.disable import DisableAbleCommandHandler

sites_list = {
    "Telegram": "https://api.telegram.org",
    "Kaizoku": "https://animekaizoku.com",
    "Kayo": "https://animekayo.com",
    "Jikan": "https://api.jikan.moe/v3"
}

PING_IMG = "https://telegra.ph/file/10e3ccea979228979cde6.jpg"

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def ping_func(to_ping: List[str]) -> List[str]:
    ping_result = []

    for each_ping in to_ping:

        start_time = time.time()
        site_to_ping = sites_list[each_ping]
        r = requests.get(site_to_ping)
        end_time = time.time()
        ping_time = str(round((end_time - start_time), 2)) + "s"

        pinged_site = f"<b>{each_ping}</b>"

        if each_ping == "Kaizoku" or each_ping == "Kayo":
            pinged_site = f'<a href="{sites_list[each_ping]}">{each_ping}</a>'
            ping_time = f"<code>{ping_time} (Status: {r.status_code})</code>"

        ping_text = f"{pinged_site}: <code>{ping_time}</code>"
        ping_result.append(ping_text)

    return ping_result


@run_async
def ping(update: Update, context: CallbackContext):
    msg = update.effective_message

    start_time = time.time()
    message = msg.reply_text("Pinging...")
    end_time = time.time()
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    uptime = get_readable_time((time.time() - StartTime))
    text = f""" 
           <b>PONG!!</b>\n<b>Time Taken:</b> <code>{telegram_ping}</code>\n<b>Service uptime:</b> <code>{uptime}</code>
           """


    update.effective_message.reply_photo(
        PING_IMG, caption=text,
        parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                  InlineKeyboardButton(text="System Stats 💻", callback_data="stats_callback")
                  ]
                ]
            ),
        )

    message.delete()

@pgram.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await pgram.answer_callback_query(CallbackQuery.id, text, show_alert=True)

@run_async
def pingall(update: Update, context: CallbackContext):
    to_ping = ["Kaizoku", "Kayo", "Telegram", "Jikan"]
    pinged_list = ping_func(to_ping)
    pinged_list.insert(2, '')
    uptime = get_readable_time((time.time() - StartTime))

    reply_msg = "⏱Ping results are:\n"
    reply_msg += "\n".join(pinged_list)
    reply_msg += '\n<b>Service uptime:</b> <code>{}</code>'.format(uptime)

    update.effective_message.reply_photo(
        PING_IMG, caption=reply_msg,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
                [
                  [
                  InlineKeyboardButton(text="System Stats 💻", callback_data="stats_callback")
                  ]
                ]
            ),
        )


PING_HANDLER = DisableAbleCommandHandler("ping", ping)
PINGALL_HANDLER = DisableAbleCommandHandler("pingall", pingall)

dispatcher.add_handler(PING_HANDLER)
dispatcher.add_handler(PINGALL_HANDLER)


__help__ = """
/ping: Miku pong
"""

__mod_name__ = "ping⚡"
__command_list__ = ["ping", "pingall"]
__handlers__ = [PING_HANDLER, PINGALL_HANDLER]
