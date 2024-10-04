from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import CallbackContext


FIRST_MENU = "<b>Menu 1</b>\n\nA beautiful menu with a shiny inline button."
SECOND_MENU = "<b>Menu 2</b>\n\nA better menu with even more shiny inline buttons."

# Pre-assign button text
NEXT_BUTTON = "Next"
BACK_BUTTON = "Back"
TUTORIAL_BUTTON = "Tutorial"

# Build keyboards
FIRST_MENU_MARKUP = InlineKeyboardMarkup(
    [[InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)]]
)
SECOND_MENU_MARKUP = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON)],
        [
            InlineKeyboardButton(
                TUTORIAL_BUTTON, url="https://core.telegram.org/bots/api"
            )
        ],
    ]
)

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Help!")

async def meme(update: Update, context: CallbackContext) -> None:
    await handle_message(update, context)

async def scream(update: Update, context: CallbackContext) -> None:
    global screaming
    screaming = True

async def whisper(update: Update, context: CallbackContext) -> None:
    global screaming
    screaming = False

async def menu(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(update.message.from_user.id, FIRST_MENU,
                                   parse_mode=ParseMode.HTML, reply_markup=FIRST_MENU_MARKUP)