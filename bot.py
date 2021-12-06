#!/usr/bin/env python

import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CommandHandler
from dbhelper import DBHelper

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

APP_NAME = 'acermj-bot'
TOKEN = '1946057696:AAH_6iuHTvbodE72vYOzBpz_QZRqyT3Aq-E'
PORT = int(os.environ.get('PORT', '8443'))

db = DBHelper()
db.setup()

# Command handlers
def start(update, context):
    update.message.reply_text('Hi!')

def help(update, context):
    update.message.reply_text('Help!')

def echo(update, context):
    update.message.reply_text("Hi there! This is the local server")
    update.message.reply_text(update.message.text)

def add_booking(update, context):
    try:
        DBHelper.add_booking("today", "kok", "morning")
        update.message.reply_text("success")
    except:
        update.message.reply_text('error')

def get_bookings(update, context):
    update.message.reply_text("Hi there! This is the local server")
    update.message.reply_text(DBHelper.get_bookings())

def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add", add_booking))
    dp.add_handler(CommandHandler("show", get_bookings))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_webhook(listen='0.0.0.0',
    port=PORT,
    url_path=TOKEN,
    webhook_url="https://acermj-bot.herokuapp.com/" + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()