import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    InlineQueryHandler,
    CallbackQueryHandler,
)
from handlers.commands import help_command, meme, scream, whisper, menu
from handlers.messages import handle_message, handle_photo, button_tap, inline_meme_query
from utils.logging import setup_logging

# 初始化日志
setup_logging()

# 主程序
if __name__ == "__main__":
    token = os.environ.get("TOKEN")
    application = ApplicationBuilder().token(token).build()

    # 添加命令和处理程序
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("meme", meme))
    application.add_handler(CommandHandler("scream", scream))
    application.add_handler(CommandHandler("whisper", whisper))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(button_tap))

    # 添加消息处理器
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(InlineQueryHandler(inline_meme_query))

    application.run_polling()