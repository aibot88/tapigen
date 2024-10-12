from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
import base64
from utils.api import generate_meme,generate_meme_url
from utils.filter import is_complete_sentence,pepe_prefix
from telegram import (
    InlineQueryResultPhoto,
)
import requests
from config.config import TOKEN, API_URL
from uuid import uuid4


async def handle_message(update: Update, context: CallbackContext) -> None:
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text="Commadn executed.")
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    prompt = pepe_prefix(update.message.text)
    try:
        img_bytes = generate_meme(prompt)
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=img_bytes)
    except Exception as e:
        print(f"generate meme error: {e}")
        await context.bot.send_message(chat_id=update.message.chat_id, text="Error generating meme.")

async def handle_photo(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.message.from_user.id,
                                   text="Msg have already sent to you, engjoy.",
                                   parse_mode=ParseMode.HTML)

async def button_tap(update: Update, context: CallbackContext) -> None:
    data = update.callback_query.data
    text = SECOND_MENU if data == NEXT_BUTTON else FIRST_MENU # type: ignore
    markup = SECOND_MENU_MARKUP if data == NEXT_BUTTON else FIRST_MENU_MARKUP # type: ignore

    await update.callback_query.answer()
    await update.callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=markup)

async def inline_meme_query(update: Update, context: CallbackContext) -> None:
    query = pepe_prefix(update.inline_query.query)
    user_first_name = update.inline_query.from_user.first_name
    print(f"[aibot-debug] {user_first_name} wrote: {query}")
    if not query or not is_complete_sentence(query):
        print(f"[aibot-debug]: not a whole sentence bypass")
        return
    inline_query_id = update.inline_query.id
    try:
        image_url = generate_meme_url(query)
        # generating_message = await context.bot.send_message(
        #     chat_id=update.inline_query.from_user.id, text="Generating... Please wait."
        # )
        # debug_image_url = "https://raw.githubusercontent.com/python-telegram-bot/logos/master/logo-text/png/ptb-logo-text_768.png"
        result = InlineQueryResultPhoto(
            id=str(uuid4()),
            photo_url=image_url,
            thumbnail_url=image_url,
            title="meme_title",
            description="prompt+label",
            # caption="Your meme is ready",
            parse_mode=ParseMode.HTML,
            photo_height=256,
            photo_width=256
            )
        print(f"[aibot debug]: result:{result}")
        await context.bot.answer_inline_query(
            inline_query_id, results=[result], cache_time=0, is_personal=True
        )
    except Exception as e:
        print(f"[aibot-debug] Error generating meme: {e}")