import html

from telegram import (
    ParseMode,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext, Filters, CommandHandler, run_async, CallbackQueryHandler
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from shizuka import (
    DEV_USERS,
    LOGGER,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
import shizuka.modules.sql.users_sql as sql
from shizuka.modules.disable import DisableAbleCommandHandler
from shizuka.modules.helper_funcs.chat_status import (
    user_admin_no_reply,
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_can_ban,
    can_delete,
)
from shizuka.modules.helper_funcs.extraction import extract_user_and_text
from shizuka.modules.helper_funcs.string_handling import extract_time
from shizuka.modules.log_channel import gloggable, loggable

UNBAN_IMG= "https://telegra.ph/file/b017dc397c6895a201170.mp4"
BAN_IMG= "https://telegra.ph/file/8feebcd2309655661e0c9.mp4"

@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot = context.bot
    args = context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ɪ ᴅᴏᴜʙᴛ ᴛʜᴀᴛ's ᴀ ᴜsᴇʀ.")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            raise
        message.reply_text("ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴘᴇʀsᴏɴ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ᴏʜ ʏᴇᴀʜ, ʙᴀɴ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
        return log_message

    if is_user_ban_protected(chat, user_id, member) and user not in DEV_USERS:
        if user_id == OWNER_ID:
            message.reply_text("ᴛʀʏɪɴɢ ᴛᴏ ᴘᴜᴛ ᴍᴇ ᴀɢᴀɪɴsᴛ ᴀ ɢᴏᴅ ʟᴇᴠᴇʟ ᴅɪsᴀsᴛᴇʀ ʜᴜʜ?")
        elif user_id in DEV_USERS:
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴀɢᴀɪɴsᴛ ᴏᴜʀ ᴏᴡɴ.")
        elif user_id in DRAGONS:
            message.reply_text(
                "ғɪɢʜᴛɪɴɢ ᴛʜɪs ᴅʀᴀɢᴏɴ ʜᴇʀᴇ ᴡɪʟʟ ᴘᴜᴛ ᴄɪᴠɪʟɪᴀɴ ʟɪᴠᴇs ᴀᴛ ʀɪsᴋ."
            )
        elif user_id in DEMONS:
            message.reply_text(
                "ʙʀɪɴɢ ᴀɴ ᴏʀᴅᴇʀ ғʀᴏᴍ ʜᴇʀᴏᴇs ᴀssᴏᴄɪᴀᴛɪᴏɴ ᴛᴏ ғɪɢʜᴛ ᴀ ᴅᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀ."
            )
        elif user_id in TIGERS:
            message.reply_text(
                "ʙʀɪɴɢ ᴀɴ ᴏʀᴅᴇʀ ғʀᴏᴍ ʜᴇʀᴏᴇs ᴀssᴏᴄɪᴀᴛɪᴏɴ ᴛᴏ ғɪɢʜᴛ ᴀ ᴛɪɢᴇʀ ᴅɪsᴀsᴛᴇʀ."
            )
        elif user_id in WOLVES:
            message.reply_text("ᴡᴏʟғ ᴀʙɪʟɪᴛɪᴇs ᴍᴀᴋᴇ ᴛʜᴇᴍ ʙᴀɴ ɪᴍᴍᴜɴᴇ!")
        else:
            message.reply_text("ᴛʜɪs ᴜsᴇʀ ʜᴀs ɪᴍᴍᴜɴɪᴛʏ ᴀɴᴅ ᴄᴀɴɴᴏᴛ ʙᴇ ʙᴀɴɴᴇᴅ.")
        return log_message
    if message.text.startswith("/s"):
        silent = True
        if not can_delete(chat, context.bot.id):
            return ""
    else:
        silent = False
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#{'S' if silent else ''}BANNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id)

        if silent:
            if message.reply_to_message:
                message.reply_to_message.delete()
            message.delete()
            return log

        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        reply = (
            f"<code>❕</code><b>ʙᴀɴ ᴇᴠᴇɴᴛ</b>\n"
            f"<code> </code><b>•  User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            reply += f"\n<code> </code><b>• Reason:</b> \n{html.escape(reason)}"

        bot.send_video(
            chat.id, BAN_IMG,caption=reply,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
       InlineKeyboardButton(text="❕Unban", callback_data=f"unbanb_unban={user_id}"),
       InlineKeyboardButton(text="❌ Delete", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
            )
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            if silent:
                return log
            message.reply_text("Baka is Banned!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR banning user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴜʜᴍ...ᴛʜᴀᴛ ᴅɪᴅɴ'ᴛ ᴡᴏʀᴋ...")

    return log_message


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def temp_ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ᴅᴜᴅᴇ! ᴀᴛ ʟᴇᴀsᴛ ʀᴇғᴇʀ sᴏᴍᴇ ᴜsᴇʀ ᴛᴏ ʙᴀɴ...")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            raise
        message.reply_text("ɪ ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ʙᴀɴ ᴍʏsᴇʟғ, ᴀʀᴇ ʏᴏᴜ ᴄʀᴀᴢʏ?")
        return log_message

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("I don't feel like it.")
        return log_message

    if not reason:
        message.reply_text("ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴘᴇᴄɪғɪᴇᴅ ᴀ ᴛɪᴍᴇ ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ ғᴏʀ!")
        return log_message

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    bantime = extract_time(message, time_val)

    if not bantime:
        return log_message

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        "#TEMP BANNED\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
        f"<b>ᴛɪᴍᴇ:</b> {time_val}"
    )
    if reason:
        log += "\n<b>ʀᴇᴀsᴏɴ:</b> {}".format(reason)

    try:
        chat.kick_member(user_id, until_date=bantime)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker

        reply_msg = (
            f"<code>❕</code><b>Temp Banned</b>\n"
            f"<code> </code><b>• User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
            f"<code> </code><b>• Banned for: {time_val}</b>"
        )

        if reason:
            reply_msg += f"\n<code> </code><b>• ʀᴇᴀsᴏɴ:</b> {html.escape(reason)}"

        bot.sendMessage(
            chat.id,
            reply_msg,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❕ᴜɴʙᴀɴ", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(text="❌ ᴅᴇʟᴇᴛᴇ", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log

    except BadRequest as excp:
        if excp.message == "ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
            # Do not reply
            message.reply_text(
                f"ʙᴀɴɴᴇᴅ! ᴜsᴇʀ ᴡɪʟʟ ʙᴇ ʙᴀɴɴᴇᴅ ғᴏʀ {time_val}.", quote=False
            )
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ᴇʀʀᴏʀ ʙᴀɴɴɪɴɢ ᴜsᴇʀ %s ɪɴ ᴄʜᴀᴛ %s (%s) ᴅᴜᴇ ᴛᴏ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜᴀᴛ ᴜsᴇʀ.")

    return log_message
    
 

    





@connection_status
@bot_admin
@can_restrict
@user_admin_no_reply
@user_can_ban
@loggable
def unbanb_btn(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user
    if query.data != "unbanb_del":
        splitter = query.data.split("=")
        query_match = splitter[0]
        if query_match == "unbanb_unban":
            user_id = splitter[1]
            if not is_user_admin(chat, int(user.id)):
                bot.answer_callback_query(
                    query.id,
                    text="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴘᴇᴏᴘʟᴇ",
                    show_alert=True,
                )
                return ""
            log_message = ""
            try:
                member = chat.get_member(user_id)
            except BadRequest:
                pass
            chat.unban_member(user_id)
            query.message.delete()
            bot.send_video(
            chat.id,
            UNBAN_IMG, caption= f"❕ᴜɴʙᴀɴ ᴇᴠᴇɴᴛ• \n👮Admin: {mention_html(user.id, user.first_name)} \n👥ᴜɴʙᴀɴ ᴜsᴇʀ: {mention_html(member.user.id, member.user.first_name)}!",
        	    parse_mode=ParseMode.HTML,
        	)
            bot.answer_callback_query(query.id, text="ᴜɴʙᴀɴɴᴇᴅ!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#UNBANNED\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
            )

    else:
        if not is_user_admin(chat, int(user.id)):
            bot.answer_callback_query(
                query.id,
                text="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛʜɪs ᴍᴇssᴀɢᴇ.",
                show_alert=True,
            )
            return ""
        query.message.delete()
        bot.answer_callback_query(query.id, text="Deleted!")
        return ""

@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def punch(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ɪ ᴅᴏᴜʙᴛ ᴛʜᴀᴛ's ᴀ ᴜsᴇʀ.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            raise

        message.reply_text("ɪ ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Yeahhh I'm not gonna do that.")
        return log_message

    if is_user_ban_protected(chat, user_id):
        message.reply_text("ɪ ʀᴇᴀʟʟʏ ᴡɪsʜ ɪ ᴄᴏᴜʟᴅ ᴘᴜɴᴄʜ ᴛʜɪs ᴜsᴇʀ....")
        return log_message

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"Removed! {mention_html(member.user.id, html.escape(member.user.first_name))}.",
            parse_mode=ParseMode.HTML,
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#KICKED\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>ʀᴇᴀsᴏɴ:</b> {reason}"

        return log

    else:
        message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ʀᴇᴍᴏᴠᴇ ᴛʜᴀᴛ ᴜsᴇʀ.")

    return log_message


@run_async
@bot_admin
@can_restrict
def punchme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("ɪ ᴡɪsʜ ɪ ᴄᴏᴜʟᴅ... ʙᴜᴛ ʏᴏᴜ'ʀᴇ ᴀɴ ᴀᴅᴍɪɴ.")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text("*ʀᴇᴍᴏᴠᴇs ʏᴏᴜ ᴏᴜᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ*")
    else:
        update.effective_message.reply_text("ʜᴜʜ? ɪ ᴄᴀɴ'ᴛ :/")


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def unban(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ɪ ᴅᴏᴜʙᴛ ᴛʜᴀᴛ's ᴀ ᴜsᴇʀ.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            raise
        message.reply_text("ɪ ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ʜᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴜɴʙᴀɴ ᴍʏsᴇʟғ ɪғ ɪ ᴡᴀsɴ'ᴛ ʜᴇʀᴇ...?")
        return log_message

    if is_user_in_chat(chat, user_id):
        message.reply_text("ɪsɴ'ᴛ ᴛʜɪs ᴘᴇʀsᴏɴ ᴀʟʀᴇᴀᴅʏ ʜᴇʀᴇ??")
        return log_message

    chat.unban_member(user_id)
    message.reply_text("ʏᴇᴘ, ᴛʜɪs ᴜsᴇʀ ᴄᴀɴ ᴊᴏɪɴ!")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"\n<b>ʀᴇᴀsᴏɴ:</b> {reason}"

    return log


@run_async
@connection_status
@bot_admin
@can_restrict
@gloggable
def selfunban(context: CallbackContext, update: Update) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    if user.id not in DRAGONS or user.id not in TIGERS:
        return

    try:
        chat_id = int(args[0])
    except:
        message.reply_text("ɢɪᴠᴇ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ.")
        return

    chat = bot.getChat(chat_id)

    try:
        member = chat.get_member(user.id)
    except BadRequest as excp:
        if excp.message == "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
            return
        else:
            raise

    if is_user_in_chat(chat, user.id):
        message.reply_text("ᴀʀᴇɴ'ᴛ ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ??")
        return

    chat.unban_member(user.id)
    message.reply_text("ʏᴇᴘ, ɪ ʜᴀᴠᴇ ᴜɴʙᴀɴɴᴇᴅ ʏᴏᴜ.")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )

    return log


        
__help__ = """
 • `/punchme`*:* punches the user who issued the command.
 • `/kickme`*:* kicks the user who issued the command.


*Muting a user commands:*
 • `/mute <userhandle>`*:* silences a user. Can also be used as a reply, muting the replied to user.
 • `/tmute <userhandle> x(m/h/d)`*:* mutes a user for x time. (via handle, or reply). `m` = `minutes`, `h` = `hours`, `d` = `days`.
 • `/unmute <userhandle>`*:* unmutes a user. Can also be used as a reply, muting the replied to user.
 
*ban a user commands:*
 • `/ban <userhandle>`*:* bans a user. (via handle, or reply)
 • `/sban <userhandle>`*:* Silently ban a user. Deletes command, Replied message and doesn't reply. (via handle, or reply)
 • `/tban <userhandle> x(m/h/d)`*:* bans a user for `x` time. (via handle, or reply). `m` = `minutes`, `h` = `hours`, `d` = `days`.
 • `/unban <userhandle>`*:* unbans a user. (via handle, or reply)
 • `/kick <userhandle>`*:* Kicks a user out of the group, (via handle, or reply)
 • `/punch <userhandle>`*:* Punches a user out of the group, (via handle, or reply)
"""

BAN_HANDLER = CommandHandler(["ban", "sban"], ban)
TEMPBAN_HANDLER = CommandHandler(["tban"], temp_ban)
PUNCH_HANDLER = CommandHandler(["punch", "kick"], punch)
UNBAN_HANDLER = CommandHandler("unban", unban)
UNBAN_BUTTON_HANDLER = CallbackQueryHandler(unbanb_btn, pattern=r"unbanb_")
ROAR_HANDLER = CommandHandler("roar", selfunban)
PUNCHME_HANDLER = DisableAbleCommandHandler(["punchme", "kickme"], punchme, filters=Filters.group)



dispatcher.add_handler(BAN_HANDLER)

dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(PUNCH_HANDLER)
dispatcher.add_handler(UNBAN_BUTTON_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(ROAR_HANDLER)
dispatcher.add_handler(PUNCHME_HANDLER)

__mod_name__ = "📛 ʙᴀɴ/ᴍᴜᴛᴇ"
__handlers__ = [
    BAN_HANDLER,

    TEMPBAN_HANDLER,
    PUNCH_HANDLER,
    UNBAN_HANDLER,
    UNBAN_BUTTON_HANDLER,
    ROAR_HANDLER,
    PUNCHME_HANDLER,
]
