import re
import random
from html import escape

import telegram
from telegram import ParseMode, InlineKeyboardMarkup, Message, InlineKeyboardButton
from telegram.error import BadRequest
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    DispatcherHandlerStop,
    CallbackQueryHandler,
    run_async,
    Filters,
)
from telegram.utils.helpers import mention_html, escape_markdown

from shizuka import dispatcher, LOGGER, DRAGONS
from shizuka.modules.disable import DisableAbleCommandHandler
from shizuka.modules.helper_funcs.handlers import MessageHandlerChecker
from shizuka.modules.helper_funcs.chat_status import user_admin
from shizuka.modules.helper_funcs.extraction import extract_text
from shizuka.modules.helper_funcs.filters import CustomFilters
from shizuka.modules.helper_funcs.misc import build_keyboard_parser
from shizuka.modules.helper_funcs.msg_types import get_filter_type
from shizuka.modules.helper_funcs.string_handling import (
    split_quotes,
    button_markdown_parser,
    escape_invalid_curly_brackets,
    markdown_to_html,
)
from shizuka.modules.sql import cust_filters_sql as sql

from shizuka.modules.connection import connected

from shizuka.modules.helper_funcs.alternate import send_message, typing_action

HANDLER_GROUP = 10

ENUM_FUNC_MAP = {
    sql.Types.TEXT.value: dispatcher.bot.send_message,
    sql.Types.BUTTON_TEXT.value: dispatcher.bot.send_message,
    sql.Types.STICKER.value: dispatcher.bot.send_sticker,
    sql.Types.DOCUMENT.value: dispatcher.bot.send_document,
    sql.Types.PHOTO.value: dispatcher.bot.send_photo,
    sql.Types.AUDIO.value: dispatcher.bot.send_audio,
    sql.Types.VOICE.value: dispatcher.bot.send_voice,
    sql.Types.VIDEO.value: dispatcher.bot.send_video,
    # sql.Types.VIDEO_NOTE.value: dispatcher.bot.send_video_note
}


@run_async
@typing_action
def list_handlers(update, context):
    chat = update.effective_chat
    user = update.effective_user

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if not conn is False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
        filter_list = "*Filter in {}:*\n"
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "Local filters"
            filter_list = "*local filters:*\n"
        else:
            chat_name = chat.title
            filter_list = "*Filters in {}*:\n"

    all_handlers = sql.get_chat_triggers(chat_id)

    if not all_handlers:
        send_message(update.effective_message,
                     "No filters saved in {}!".format(chat_name))
        return

    for keyword in all_handlers:
        entry = " • `{}`\n".format(escape_markdown(keyword))
        if len(entry) + len(filter_list) > telegram.MAX_MESSAGE_LENGTH:
            send_message(
                update.effective_message,
                filter_list.format(chat_name),
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
            filter_list = entry
        else:
            filter_list += entry

    send_message(
        update.effective_message,
        filter_list.format(chat_name),
        parse_mode=telegram.ParseMode.MARKDOWN,
    )


# NOT ASYNC BECAUSE DISPATCHER HANDLER RAISED
@user_admin
@typing_action
def filters(update, context):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    args = msg.text.split(
        None,
        1)  # use python's maxsplit to separate Cmd, keyword, and reply_text

    conn = connected(context.bot, update, chat, user.id)
    if not conn is False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "local filters"
        else:
            chat_name = chat.title

    if not msg.reply_to_message and len(args) < 2:
        send_message(
            update.effective_message,
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏʙᴏᴀʀᴅ ᴋᴇʏᴡᴏʀᴅ ғᴏʀ ᴛʜɪs ғɪʟᴛᴇʀ ᴛᴏ ʀᴇᴘʟʏ ᴡɪᴛʜ!",
        )
        return

    if msg.reply_to_message:
        if len(args) < 2:
            send_message(
                update.effective_message,
                "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏᴡᴏʀᴅ ғᴏʀ ᴛʜɪs ғɪʟᴛᴇʀ ᴛᴏ ʀᴇᴘʟʏ ᴡɪᴛʜ!",
            )
            return
        else:
            keyword = args[1]
    else:
        extracted = split_quotes(args[1])
        if len(extracted) < 1:
            return
        # set trigger -> lower, so as to avoid adding duplicate filters with different cases
        keyword = extracted[0].lower()

    # Add the filter
    # Note: perhaps handlers can be removed somehow using sql.get_chat_filters
    for handler in dispatcher.handlers.get(HANDLER_GROUP, []):
        if handler.filters == (keyword, chat_id):
            dispatcher.remove_handler(handler, HANDLER_GROUP)

    text, file_type, file_id = get_filter_type(msg)
    if not msg.reply_to_message and len(extracted) >= 2:
        offset = len(extracted[1]) - len(
            msg.text)  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            extracted[1], entities=msg.parse_entities(), offset=offset)
        text = text.strip()
        if not text:
            send_message(
                update.effective_message,
                "ᴛʜᴇʀᴇ ɪs ɴᴏ ɴᴏᴛᴇ ᴍᴇssᴀɢᴇ - ʏᴏᴜ ᴄᴀɴ'ᴛ ᴊᴜsᴛ ʜᴀᴠᴇ ʙᴜᴛᴛᴏɴs, ʏᴏᴜ ɴᴇᴇᴅ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴏ ᴡɪᴛʜ ɪᴛ!",
            )
            return

    elif msg.reply_to_message and len(args) >= 2:
        if msg.reply_to_message.text:
            text_to_parsing = msg.reply_to_message.text
        elif msg.reply_to_message.caption:
            text_to_parsing = msg.reply_to_message.caption
        else:
            text_to_parsing = ""
        offset = len(text_to_parsing
                    )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            text_to_parsing, entities=msg.parse_entities(), offset=offset)
        text = text.strip()

    elif not text and not file_type:
        send_message(
            update.effective_message,
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏᴡᴏʀᴅ ғᴏʀ ᴛʜɪs ғɪʟᴛᴇʀ ʀᴇᴘʟʏ ᴡɪᴛʜ!",
        )
        return

    elif msg.reply_to_message:
        if msg.reply_to_message.text:
            text_to_parsing = msg.reply_to_message.text
        elif msg.reply_to_message.caption:
            text_to_parsing = msg.reply_to_message.caption
        else:
            text_to_parsing = ""
        offset = len(text_to_parsing
                    )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            text_to_parsing, entities=msg.parse_entities(), offset=offset)
        text = text.strip()
        if (msg.reply_to_message.text or
                msg.reply_to_message.caption) and not text:
            send_message(
                update.effective_message,
                "ᴛʜᴇʀᴇ ɪs ɴᴏ ɴᴏᴛᴇ ᴍᴇssᴀɢᴇ - ʏᴏᴜ ᴄᴀɴ'ᴛ ᴊᴜsᴛ ʜᴀᴠᴇ ʙᴜᴛᴛᴏɴs, ʏᴏᴜ ɴᴇᴇᴅ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴏ ᴡɪᴛʜ ɪᴛ!",
            )
            return

    else:
        send_message(update.effective_message, "Invalid filter!")
        return

    add = addnew_filter(update, chat_id, keyword, text, file_type, file_id,
                        buttons)
    # This is an old method
    # sql.add_filter(chat_id, keyword, content, is_sticker, is_document, is_image, is_audio, is_voice, is_video, buttons)

    if add is True:
        send_message(
            update.effective_message,
            "Saved filter '{}' in *{}*!".format(keyword, chat_name),
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    raise DispatcherHandlerStop


# NOT ASYNC BECAUSE DISPATCHER HANDLER RAISED
@user_admin
@typing_action
def stop_filter(update, context):
    chat = update.effective_chat
    user = update.effective_user
    args = update.effective_message.text.split(None, 1)

    conn = connected(context.bot, update, chat, user.id)
    if not conn is False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "Local filters"
        else:
            chat_name = chat.title

    if len(args) < 2:
        send_message(update.effective_message, "ᴡʜᴀᴛ sʜᴏᴜʟᴅ ɪ sᴛᴏᴘ?")
        return

    chat_filters = sql.get_chat_triggers(chat_id)

    if not chat_filters:
        send_message(update.effective_message, "ɴᴏ ғɪʟᴛᴇʀs ᴀᴄᴛɪᴠᴇ ʜᴇʀᴇ!")
        return

    for keyword in chat_filters:
        if keyword == args[1]:
            sql.remove_filter(chat_id, args[1])
            send_message(
                update.effective_message,
                "ᴏᴋᴀʏ, ɪ'ʟʟ sᴛᴏᴘ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴀᴛ ғɪʟᴛᴇʀ ɪɴ *{}*.".format(
                    chat_name),
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
            raise DispatcherHandlerStop

    send_message(
        update.effective_message,
        "ᴛʜᴀᴛ's ɴᴏᴛ ᴀ ғɪʟᴛᴇʀ - ᴄʟɪᴄᴋ: /filters ᴛᴏ ɢᴇᴛ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ғɪʟᴛᴇʀs.",
    )


@run_async
def reply_filter(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]

    if not update.effective_user or update.effective_user.id == 777000:
        return
    to_match = extract_text(message)
    if not to_match:
        return

    chat_filters = sql.get_chat_triggers(chat.id)
    for keyword in chat_filters:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            if MessageHandlerChecker.check_user(update.effective_user.id):
                return
            filt = sql.get_filter(chat.id, keyword)
            if filt.reply == "there is should be a new reply":
                buttons = sql.get_buttons(chat.id, filt.keyword)
                keyb = build_keyboard_parser(context.bot, chat.id, buttons)
                keyboard = InlineKeyboardMarkup(keyb)

                VALID_WELCOME_FORMATTERS = [
                    "first",
                    "last",
                    "fullname",
                    "username",
                    "id",
                    "chatname",
                    "mention",
                ]
                if filt.reply_text:
                    if '%%%' in filt.reply_text:
                        split = filt.reply_text.split('%%%')
                        if all(split):
                            text = random.choice(split)
                        else:
                            text = filt.reply_text
                    else:
                        text = filt.reply_text
                    if text.startswith('~!') and text.endswith('!~'):
                        sticker_id = text.replace('~!', '').replace('!~', '')
                        try:
                            context.bot.send_sticker(
                                chat.id,
                                sticker_id,
                                reply_to_message_id=message.message_id)
                            return
                        except BadRequest as excp:
                            if excp.message == 'ᴡʀᴏɴɢ ʀᴇᴍᴏᴛᴇ ғɪʟᴇ ɪᴅᴇɴᴛɪғɪᴇʀ sᴘᴇᴄɪғɪᴇᴅ: ᴡʀᴏɴɢ ᴘᴀᴅᴅɪɴɢ ɪɴ ᴛʜᴇ sᴛʀɪɴɢ':
                                context.bot.send_message(
                                    chat.id,
                                    "ᴍᴇssᴀɢᴇ ᴄᴏᴜʟᴅɴ'ᴛ ʙᴇ sᴇɴᴛ, ɪs ᴛʜᴇ sᴛɪᴄᴋᴇʀ ɪᴅ ᴠᴀʟɪᴅ?"
                                )
                                return
                            else:
                                LOGGER.exception("Error in filters: " +
                                                 excp.message)
                                return
                    valid_format = escape_invalid_curly_brackets(
                        text, VALID_WELCOME_FORMATTERS)
                    if valid_format:
                        filtext = valid_format.format(
                            first=escape(message.from_user.first_name),
                            last=escape(message.from_user.last_name or
                                        message.from_user.first_name),
                            fullname=" ".join(
                                [
                                    escape(message.from_user.first_name),
                                    escape(message.from_user.last_name),
                                ] if message.from_user.last_name else
                                [escape(message.from_user.first_name)]),
                            username="@" + escape(message.from_user.username)
                            if message.from_user.username else mention_html(
                                message.from_user.id,
                                message.from_user.first_name),
                            mention=mention_html(message.from_user.id,
                                                 message.from_user.first_name),
                            chatname=escape(message.chat.title)
                            if message.chat.type != "private" else escape(
                                message.from_user.first_name),
                            id=message.from_user.id,
                        )
                    else:
                        filtext = ""
                else:
                    filtext = ""

                if filt.file_type in (sql.Types.BUTTON_TEXT, sql.Types.TEXT):
                    try:
                        context.bot.send_message(
                            chat.id,
                            markdown_to_html(filtext),
                            reply_to_message_id=message.message_id,
                            parse_mode=ParseMode.HTML,
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )
                    except BadRequest as excp:
                        error_catch = get_exception(excp, filt, chat)
                        if error_catch == "noreply":
                            try:
                                context.bot.send_message(
                                    chat.id,
                                    markdown_to_html(filtext),
                                    parse_mode=ParseMode.HTML,
                                    disable_web_page_preview=True,
                                    reply_markup=keyboard,
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Error in filters: " +
                                                 excp.message)
                                send_message(
                                    update.effective_message,
                                    get_exception(excp, filt, chat),
                                )
                        else:
                            try:
                                send_message(
                                    update.effective_message,
                                    get_exception(excp, filt, chat),
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Failed to send message: " +
                                                 excp.message)
                                pass
                else:
                    try:
                        ENUM_FUNC_MAP[filt.file_type](
                            chat.id,
                            filt.file_id,
                            caption=markdown_to_html(filtext),
                            reply_to_message_id=message.message_id,
                            parse_mode=ParseMode.HTML,
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )
                    except BadRequest:
                        send_message(
                            message,
                            "ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ ᴏғ ᴛʜᴇ ғɪʟᴛᴇʀ."
                        )
                break
            else:
                if filt.is_sticker:
                    message.reply_sticker(filt.reply)
                elif filt.is_document:
                    message.reply_document(filt.reply)
                elif filt.is_image:
                    message.reply_photo(filt.reply)
                elif filt.is_audio:
                    message.reply_audio(filt.reply)
                elif filt.is_voice:
                    message.reply_voice(filt.reply)
                elif filt.is_video:
                    message.reply_video(filt.reply)
                elif filt.has_markdown:
                    buttons = sql.get_buttons(chat.id, filt.keyword)
                    keyb = build_keyboard_parser(context.bot, chat.id, buttons)
                    keyboard = InlineKeyboardMarkup(keyb)

                    try:
                        send_message(
                            update.effective_message,
                            filt.reply,
                            parse_mode=ParseMode.MARKDOWN,
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )
                    except BadRequest as excp:
                        if excp.message == "Unsupported url protocol":
                            try:
                                send_message(
                                    update.effective_message,
                                    "ʏᴏᴜ sᴇᴇᴍ ᴛᴏ ʙᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴜsᴇ ᴀɴ ᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ᴜʀʟ ᴘʀᴏᴛᴏᴄᴏʟ. "
                                    "ᴛᴇʟᴇɢʀᴀᴍ ᴅᴏᴇsɴ'ᴛ sᴜᴘᴘᴏʀᴛ ʙᴜᴛᴛᴏɴs ғᴏʀ sᴏᴍᴇ ᴘʀᴏᴛᴏᴄᴏʟs, sᴜᴄʜ ᴀs tg://. ᴘʟᴇᴀsᴇ ᴛʀʏ "
                                    "ᴀɢᴀɪɴ...",
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Error in filters: " +
                                                 excp.message)
                                pass
                        elif excp.message == "ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
                            try:
                                context.bot.send_message(
                                    chat.id,
                                    filt.reply,
                                    parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True,
                                    reply_markup=keyboard,
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Error in filters: " +
                                                 excp.message)
                                pass
                        else:
                            try:
                                send_message(
                                    update.effective_message,
                                    "ᴛʜɪs ᴍᴇssᴀɢᴇ ᴄᴏᴜʟᴅɴ'ᴛ ʙᴇ sᴇɴᴛ ᴀs ɪᴛ's ɪɴᴄᴏʀʀᴇᴄᴛʟʏ ғᴏʀᴍᴀᴛᴛᴇᴅ.",
                                )
                            except BadRequest as excp:
                                LOGGER.exception("Error in filters: " +
                                                 excp.message)
                                pass
                            LOGGER.warning("Message %s ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ᴘᴀʀsᴇᴅ",
                                           str(filt.reply))
                            LOGGER.exception(
                                "Could not parse filter %s in chat %s",
                                str(filt.keyword),
                                str(chat.id),
                            )

                else:
                    # LEGACY - all new filters will have has_markdown set to True.
                    try:
                        send_message(update.effective_message, filt.reply)
                    except BadRequest as excp:
                        LOGGER.exception("Error in filters: " + excp.message)
                        pass
                break


@run_async
def rmall_filters(update, context):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in DRAGONS:
        update.effective_message.reply_text(
            "Only the chat owner can clear all notes at once.")
    else:
        buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Stop all filters", callback_data="filters_rmall")
        ], [
            InlineKeyboardButton(text="Cancel", callback_data="filters_cancel")
        ]])
        update.effective_message.reply_text(
            f"ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ sᴛᴏᴘ ᴀʟʟ ғɪʟᴛᴇʀs ɪɴ {chat.title}? ᴛʜɪs ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN)


@run_async
def rmall_callback(update, context):
    query = update.callback_query
    chat = update.effective_chat
    msg = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == 'filters_rmall':
        if member.status == "creator" or query.from_user.id in DRAGONS:
            allfilters = sql.get_chat_triggers(chat.id)
            if not allfilters:
                msg.edit_text("ɴᴏ ғɪʟᴛᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ, ɴᴏᴛʜɪɴɢ ᴛᴏ sᴛᴏᴘ!")
                return

            count = 0
            filterlist = []
            for x in allfilters:
                count += 1
                filterlist.append(x)

            for i in filterlist:
                sql.remove_filter(chat.id, i)

            msg.edit_text(f"ᴄʟᴇᴀɴᴇᴅ {count} ғɪʟᴛᴇʀs ɪɴ {chat.title}")

        if member.status == "administrator":
            query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪs.")

        if member.status == "member":
            query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs.")
    elif query.data == 'filters_cancel':
        if member.status == "creator" or query.from_user.id in DRAGONS:
            msg.edit_text("ᴄʟᴇᴀʀɪɴɢ ᴏғ ᴀʟʟ ғɪʟᴛᴇʀs ʜᴀs ʙᴇᴇɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
            return
        if member.status == "administrator":
            query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪs.")
        if member.status == "member":
            query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs.")


# NOT ASYNC NOT A HANDLER
def get_exception(excp, filt, chat):
    if excp.message == "Unsupported url protocol":
        return "ʏᴏᴜ sᴇᴇᴍ ᴛᴏ ʙᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴜsᴇ ᴛʜᴇ ᴜʀʟ ᴘʀᴏᴛᴏᴄᴏʟ ᴡʜɪᴄʜ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ. ᴛᴇʟᴇɢʀᴀᴍ ᴅᴏᴇs ɴᴏᴛ sᴜᴘᴘᴏʀᴛ ᴋᴇʏ ғᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴘʀᴏᴛᴏᴄᴏʟs, sᴜᴄʜ ᴀs tg: //. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ!"
    elif excp.message == "ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
        return "noreply"
    else:
        LOGGER.warning("Message %s could not be parsed", str(filt.reply))
        LOGGER.exception("Could not parse filter %s in chat %s",
                         str(filt.keyword), str(chat.id))
        return "ᴛʜɪs ᴅᴀᴛᴀ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ sᴇɴᴛ ʙᴇᴄᴀᴜsᴇ ɪᴛ ɪs ɪɴᴄᴏʀʀᴇᴄᴛʟʏ ғᴏʀᴍᴀᴛᴛᴇᴅ."


# NOT ASYNC NOT A HANDLER
def addnew_filter(update, chat_id, keyword, text, file_type, file_id, buttons):
    msg = update.effective_message
    totalfilt = sql.get_chat_triggers(chat_id)
    if len(totalfilt) >= 150:  # Idk why i made this like function....
        msg.reply_text("ᴛʜɪs ɢʀᴏᴜᴘ ʜᴀs ʀᴇᴀᴄʜᴇᴅ ɪᴛs ᴍᴀx ғɪʟᴛᴇʀs ʟɪᴍɪᴛ ᴏғ 𝟷𝟻𝟶.")
        return False
    else:
        sql.new_add_filter(chat_id, keyword, text, file_type, file_id, buttons)
        return True


def __stats__():
    return "• {} filters, across {} chats.".format(sql.num_filters(),
                                                   sql.num_chats())


def __import_data__(chat_id, data):
    # set chat filters
    filters = data.get("filters", {})
    for trigger in filters:
        sql.add_to_blacklist(chat_id, trigger)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    cust_filters = sql.get_chat_triggers(chat_id)
    return "ᴛʜᴇʀᴇ ᴀʀᴇ `{}` ᴄᴜsᴛᴏᴍ ғɪʟᴛᴇʀs ʜᴇʀᴇ.".format(len(cust_filters))


__help__ = """
 • `/filters`*:* List all active filters saved in the chat.

*Admin only:*
 • `/filter <keyword> <reply message>`*:* Add a filter to this chat. The bot will now reply that message whenever 'keyword'\
is mentioned. If you reply to a sticker with a keyword, the bot will reply with that sticker. NOTE: all filter \
keywords are in lowercase. If you want your keyword to be a sentence, use quotes. eg: /filter "hey there" How you \
doin?
 Separate diff replies by `%%%` to get random replies
 *Example:* 
 `/filter "filtername"
 Reply 1
 %%%
 Reply 2
 %%%
 Reply 3`
 • `/stop <filter keyword>`*:* Stop that filter.

*Chat creator only:*
 • `/removeallfilters`*:* Remove all chat filters at once.

*Note*: Filters also support markdown formatters like: {first}, {last} etc.. and buttons.
Check `/markdownhelp` to know more!

"""

__mod_name__ = "💫 ғɪʟᴛᴇʀ"

FILTER_HANDLER = CommandHandler("filter", filters)
STOP_HANDLER = CommandHandler("stop", stop_filter)
RMALLFILTER_HANDLER = CommandHandler(
    "removeallfilters", rmall_filters, filters=Filters.group)
RMALLFILTER_CALLBACK = CallbackQueryHandler(
    rmall_callback, pattern=r"filters_.*")
LIST_HANDLER = DisableAbleCommandHandler(
    "filters", list_handlers, admin_ok=True)
CUST_FILTER_HANDLER = MessageHandler(
    CustomFilters.has_text & ~Filters.update.edited_message, reply_filter)

dispatcher.add_handler(FILTER_HANDLER)
dispatcher.add_handler(STOP_HANDLER)
dispatcher.add_handler(LIST_HANDLER)
dispatcher.add_handler(CUST_FILTER_HANDLER, HANDLER_GROUP)
dispatcher.add_handler(RMALLFILTER_HANDLER)
dispatcher.add_handler(RMALLFILTER_CALLBACK)

__handlers__ = [
    FILTER_HANDLER, STOP_HANDLER, LIST_HANDLER,
    (CUST_FILTER_HANDLER, HANDLER_GROUP, RMALLFILTER_HANDLER)
]
