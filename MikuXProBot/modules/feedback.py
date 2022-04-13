import random

from telegram import ParseMode
from telethon import Button

from MikuXProBot import OWNER_ID, SUPPORT_CHAT
from MikuXProBot import telethn as tbot
from MikuXProBot.events import register

SHU1 = ( "https://telegra.ph/file/3cd1f5776c3ea08f609f4.jpg", 
      "https://telegra.ph/file/e384ab52db8c0912ca356.jpg", 
      "https://telegra.ph/file/0adf9e97735ba8a420973.jpg", 
      "https://telegra.ph/file/2861eda5afba02bf04254.jpg", 
      "https://telegra.ph//file/f218b08b076fa31df028b.jpg", 
      "https://telegra.ph//file/75280e721b12b8b4a18a4.jpg", 
      "https://telegra.ph/file/3cd1f5776c3ea08f609f4.jpg", 
      "https://telegra.ph/file/e384ab52db8c0912ca356.jpg", 
      "https://telegra.ph/file/0adf9e97735ba8a420973.jpg"  
      "https://telegra.ph/file/2861eda5afba02bf04254.jpg", 
      "https://telegra.ph//file/75280e721b12b8b4a18a4.jpg", 
      "https://telegra.ph//file/8cddbaed2a1718c935f83.jpg", 
      ) 
SHU2 = "https://telegra.ph//file/1247053aadf93e8e371a2.jpg"

@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    BUTTON = [[Button.url("Go To Support Group", f"https://t.me/SHUKURENAI_SUPPORT")]]
    TEXT = "Thanks For Your Feedback, I Hope You Happy With Our Service"
    GIVE = "Give Some Text For Feedback ✨"
    logger_text = f"""
**New Feedback**

**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=SHU2,
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(SHU1),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(SHU1), buttons=BUTTON)

__help__ = """
 - /feedback : You can give us your feedbacks 
               can can see your feeds here.
"""

__mod_name__ = "feedback"
