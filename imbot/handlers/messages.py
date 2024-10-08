from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
import base64
from utils.api import generate_meme
from utils.filter import is_complete_sentence
from telegram import (
    InlineQueryResultPhoto,
)
import requests
from config.config import TOKEN, API_URL
from uuid import uuid4


async def handle_message(update: Update, context: CallbackContext) -> None:
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text="命令已执行！")
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    prompt = update.message.text
    try:
        img_bytes = generate_meme(prompt)
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=img_bytes)
    except Exception as e:
        print(f"generate meme error: {e}")
        await context.bot.send_message(chat_id=update.message.chat_id, text="Error generating meme.")

async def handle_photo(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.message.from_user.id,
                                   text="图片已发送给你，请确认后再发送到群里。",
                                   parse_mode=ParseMode.HTML)

async def button_tap(update: Update, context: CallbackContext) -> None:
    data = update.callback_query.data
    text = SECOND_MENU if data == NEXT_BUTTON else FIRST_MENU
    markup = SECOND_MENU_MARKUP if data == NEXT_BUTTON else FIRST_MENU_MARKUP

    await update.callback_query.answer()
    await update.callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=markup)


async def generate_meme_key(prompt, image_count=1, random_seed=42):
    """
    通过后端 API 生成 meme，并返回生成的 meme 的 MongoDB ID 列表。
    """
    prompt = "pepe: " + prompt
    GENERATE_API_URL = API_URL + "/generate"
    response = requests.post(
        GENERATE_API_URL,
        json={"prompt": prompt, "image_count": image_count, "random_seed": random_seed},
    )

    if response.status_code == 200:
        data = response.json()
        return data["keys"]
    else:
        print(f"[aibot-debug] Error generating meme: {response.text}")
        return []

async def inline_meme_query(update: Update, context: CallbackContext) -> None:
    GET_MEME_API_URL = API_URL + "/get_meme/{key}"
    query = update.inline_query.query
    user_first_name = update.inline_query.from_user.first_name

    print(f"[aibot-debug] {user_first_name} wrote: {query}")

    # 如果没有输入内容，则不返回结果
    if not query or not is_complete_sentence(query):
        print(f"[aibot-debug]: not a whole sentence bypass")
        return
    inline_query_id = update.inline_query.id

    try:
        meme_keys = await generate_meme_key(query)
        # 先回复 "generating..." 消息
        generating_message = await context.bot.send_message(
            chat_id=update.inline_query.from_user.id, text="Generating... Please wait."
        )
        # meme_keys = ['meme_key']

        if meme_keys:
            results = []
            for meme_key in meme_keys:
                image_url = GET_MEME_API_URL.format(key=meme_key)
                # debug_image_url = "https://tapi.theemogen.com/get_meme/66f972d3fe43c6aad22c15fc.jpg"
                # debug_image_url = "https://raw.githubusercontent.com/python-telegram-bot/logos/master/logo-text/png/ptb-logo-text_768.png"
                result = InlineQueryResultPhoto(
                    id=str(uuid4()),
                    photo_url=image_url,
                    thumbnail_url=image_url,
                    title="meme_title",
                    description="prompt+label",
                    caption="Your meme is ready",
                    parse_mode=ParseMode.HTML,
                    photo_height=256,
                    photo_width=256
                    )
                results.append(result)
                print(f"[aibot debug]: result:{result}")

            await context.bot.edit_message_text(
                chat_id=generating_message.chat.id,
                message_id=generating_message.message_id,
                text="Here is your meme!",
            )
            await context.bot.answer_inline_query(
                inline_query_id, results=results, cache_time=0, is_personal=True
            )
        else:
            await context.bot.answer_inline_query(
                inline_query_id, results=[], cache_time=0, is_personal=True
            )

    except Exception as e:
        print(f"[aibot-debug] Error generating meme: {e}")