# Miku Example plugin format

## Advanced: Decorators
```python3

from MikuXProBot.modules.helper_funcs.decorators import mikucmd
from telegram import Update
from telegram.ext import CallbackContext

@mikucmd(command='hi', pass_args=True)
def hello(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text("hello")

    
__mod_name__ = "Hi"
__help__ = """
<b>Hi</b>
- /hi: Say Hello There
"""
```



## Advanced: Pyrogram
```python3
from MikuXProBot import pgram

@pgram.on_message(filters.command("hi") & ~filters.edited & ~filters.bot)
async def hmm(client, message):
    j = "Hello there"
    await message.reply(j)
    
__mod_name__ = "Hi"
__help__ = """
<b>Hi</b>
- /hi: Say Hello There
"""
```

## Advanced: Telethon
```python3

from MikuXProBot import telethn
from MikuXProBot.events import register

@register(pattern="^/hi$")
async def hmm(event):
    j = "Hello there"
    await event.reply(j)
    
__mod_name__ = "Hi"
__help__ = """
<b>Hi</b>
- /hi: Say Hello There
"""
```

## Advanced: PTB
```python3

from MikuXProBot import dispatcher
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

def hi(update: Update, context: CallbackContext):
    j = "hello"
    update.effective_message.reply_text(j)

HANDLER = CommandHandler("hi", hi, run_async=True)
dispatcher.add_handler(HANDLER)

__handlers__ = [ HANDLER, ]
    
__mod_name__ = "Hi"
__help__ = """
<b>Hi</b>
- /hi: Say Hello There
"""
```
