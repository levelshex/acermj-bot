#!/usr/bin/env python

import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

APP_NAME = 'AcerMJ'
TOKEN = '1946057696:AAH_6iuHTvbodE72vYOzBpz_QZRqyT3Aq-E'
PORT = int(os.environ.get('PORT', '8443'))

# Command handlers
def start(update, context):
    update.message.reply_text('Hi!')

def help(update, context):
    update.message.reply_text('Help!')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_webhook(listen='0.0.0.0',
    port=PORT,
    url_path=TOKEN)
    updater.bot.set_webhook(APP_NAME + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()