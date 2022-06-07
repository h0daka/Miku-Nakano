import requests
from MikuXProBot import dispatcher
from MikuXProBot.modules.disable import DisableAbleCommandHandler
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update)
from telegram.ext import CallbackContext


def ud(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text[len('/ud '):]
    results = requests.get(
        f'https://api.urbandictionary.com/v0/define?term={text}').json()
    try:
        reply_text = f'*⚠️ Warning:* Urban Dictionary does not always provide accurate descriptions\n\n*• Word :* `{text}`\n\n*• Meaning :* _{results["list"][0]["definition"]}\n_\n*• Example:* _{results["list"][0]["example"]}_'
    except:
        reply_text = "No results found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                  [                  
                       InlineKeyboardButton(
                             text="🔎 Google it!",
                             url=f"https://www.google.com/search?q=define+{text}")
                     ] 
                ]
            ),
         )


UD_HANDLER = DisableAbleCommandHandler(["ud"], ud, run_async=True)

dispatcher.add_handler(UD_HANDLER)

__help__ = """
/ud: an definition for you word
"""

__mod_name__ = "ud🗒️"
__command_list__ = ["ud"]
__handlers__ = [UD_HANDLER]
