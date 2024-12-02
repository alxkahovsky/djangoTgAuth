#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import httpx

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    token = context.args[0] if context.args else None
    if token:
        telegram_id = update.effective_user.id
        url = "http://django:8000/auth/complete/"
        data = {"token": token, "telegram_id": user.id, "telegram_username": user.username}
        response = httpx.post(url, data=data)
        logger.info(response.status_code)
        await update.message.reply_html(
            rf"Hi {user.mention_html()} \ {token} \ {user.id} \ {user.username}!",
            reply_markup=ForceReply(selective=True),
        )
    else:
        pass


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    token = os.environ.get("TOKEN", "TOKEN")
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

# def start(update: Update, context: CallbackContext) -> None:
#     token = context.args[0] if context.args else None
#     if token:
#         telegram_id = update.effective_user.id
#         update.message.reply_text(f'Авторизация прошла успешно! {telegram_id}')
#     #     response = requests.post('http://django_tg_app/auth/api/verify_token/', data={'token': token, 'telegram_id': telegram_id})
#     #     if response.json().get('status') == 'success':
#     #         update.message.reply_text('Авторизация прошла успешно!')
#     #     else:
#     #         update.message.reply_text('Токен не найден.')
#     # else:
#     #     update.message.reply_text('Неверный формат команды.')
#
