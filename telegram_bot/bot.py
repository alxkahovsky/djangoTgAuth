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

from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import os
import httpx
from sdk import SiteAuthConnector

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    token = context.args[0] if context.args else None

    if token:
        context.user_data['token'] = token
        keyboard = [
            [InlineKeyboardButton("Да", callback_data="yes")],
            [InlineKeyboardButton("Нет", callback_data="no")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_html(
            rf"Hi {user.mention_html()} {user.id}! Do you want to proceed with token {token}?",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_html(
            "Please provide a token after the /start command, e.g., /start your_token"
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button press."""
    query = update.callback_query
    await query.answer()

    if query.data == 'yes':
        token = context.user_data.get('token')
        if token:
            try:
                telegram_id = update.effective_user.id
                site = SiteAuthConnector(os.environ.get("SITE_AUTH_URL", "http://localhost:8000"))
                site.complete_auth(telegram_id=str(telegram_id), username=update.effective_user.username, session_key=token)
                await update.message.reply_text(text=f"Авторизация прошла успешно!")
            except Exception as e:
                logger.error(f"{e}")
                await update.message.reply_text(text=f"Ошибка авторизации")
        else:
            logger.info("Token not found.")
            await update.message.reply_text(text=f"Ошибка авторизации")
    elif query.data == 'no':
        await update.message.reply_text(text="Операция отменена")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    token = os.environ.get("TOKEN", "TOKEN")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
