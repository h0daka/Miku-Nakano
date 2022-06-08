import re
import html

from telegram import ParseMode
from telegram.update import Update
from telegram.ext import ChatJoinRequestHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.utils.helpers import mention_html

from MikuXProBot.modules.helper_funcs.anonymous import AdminPerms, user_admin

from MikuXProBot.import dispatcher
from MikuXProBot.modules.helper_funcs.decorators import mikucallback

from MikuXProBot.modules.log_channel import loggable


def chat_join_req(upd: Update, ctx: CallbackContext):
    bot = ctx.bot
    user = upd.chat_join_request.from_user
    chat = upd.chat_join_request.chat
    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            "✅ Approve", callback_data="cb_approve={}".format(user.id)
                    ),
                    InlineKeyboardButton(
                            "❌ Decline", callback_data="cb_decline={}".format(user.id)
                    ),
                ]
            ]
    )
    bot.send_message(
            chat.id,
            "{} wants to join {}".format(
                    mention_html(user.id, user.first_name), chat.title or "this chat"
            ),
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
    )


@mikucallback(pattern=r"cb_approve=")
@user_admin(AdminPerms.CAN_INVITE_USERS, noreply=True)
@loggable
def approve_joinReq(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    match = re.match(r"cb_approve=(.+)", query.data)

    user_id = match.group(1)
    try:
        bot.approve_chat_join_request(chat.id, user_id)
        joined_user = bot.get_chat_member(chat.id, user_id)
        joined_mention = mention_html(user_id, html.escape(joined_user.user.first_name))
        admin_mention = mention_html(user.id, html.escape(user.first_name))
        update.effective_message.edit_text(
                f"{joined_mention}'s join request was approved by {admin_mention}.",
                parse_mode="HTML",
        )
        logmsg = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#JOIN_REQUEST\n"
            f"Approved\n"
            f"<b>Admin:</b> {admin_mention}\n"
            f"<b>User:</b> {joined_mention}\n"
        )
        return logmsg
    except Exception as e:
        update.effective_message.edit_text(str(e))
        pass


@mikucallback(pattern=r"cb_decline=")
@user_admin(AdminPerms.CAN_INVITE_USERS, noreply=True)
@loggable
def decline_joinReq(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    match = re.match(r"cb_decline=(.+)", query.data)

    user_id = match.group(1)
    try:
        bot.decline_chat_join_request(chat.id, user_id)
        joined_user = bot.get_chat_member(chat.id, user_id)
        joined_mention = mention_html(user_id, html.escape(joined_user.user.first_name))
        admin_mention = mention_html(user.id, html.escape(user.first_name))
        update.effective_message.edit_text(
                f"{joined_mention}'s join request was declined by {admin_mention}.",
                parse_mode="HTML",
        )
        logmsg = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#JOIN_REQUEST\n"
            f"Declined\n"
            f"<b>Admin:</b> {admin_mention}\n"
            f"<b>User:</b> {joined_mention}\n"
        )
        return logmsg
    except Exception as e:
        update.effective_message.edit_text(str(e))
        pass


dispatcher.add_handler(ChatJoinRequestHandler(callback=chat_join_req, run_async=True))
