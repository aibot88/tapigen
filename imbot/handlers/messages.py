from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
import base64
from utils.api import generate_meme

async def handle_message(update: Update, context: CallbackContext) -> None:
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text="命令已执行！")
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    prompt = update.message.text
    image_base64 = generate_meme(prompt)

    if image_base64:
        image_data = base64.b64decode(image_base64)
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=image_data)
    else:
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

async def inline_meme_query(update: Update, context: CallbackContext) -> None:
    # 处理 inline query 逻辑
    pass