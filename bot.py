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
    update.message.reply_text(parse_mode='Markdown',
                              text="\"*/add <date> <start time> <end time> <table_type(optional)>*\" to add a booking.\n\"*/delete <date> <start time>*\" to delete a booking.\n<date> in \"YYYY-MM-DD\" format.\n<time> in \"HH:MM\" format.\n<table_type> either 'auto', 'normal' or 'other', 'auto' will be chosen if not specified.")
def echo(update, context):
    update.message.reply_text("Hi there! This is the local server")
    update.message.reply_text(update.message.text)

def add_booking(update, context):
    try:
        name = update.message.from_user["username"]
        db = DBHelper()
        if True:
            if len(context.args) == 4:
                db.add_booking(context.args[0], name, context.args[1] + ":00", context.args[2] + ":00", context.args[3])
            else:
                db.add_booking(context.args[0], name, context.args[1] + ":00", context.args[2] + ":00", 'auto')
        else:
            update.message.reply_text(
                "/add <date> <start time> <end time> <table_type(optional)>\n e.g /add 2021-01-31 15:00 19:00 normal")
        print("added")
        get_bookings(update, context)
    except:
        update.message.reply_text('error')

def get_bookings(update, context):
    try:
        db = DBHelper()
        bookings = db.get_bookings()
        stmt = ''
        if bookings:
            stmt += "*AUTO TABLE*"
            for booking in bookings['auto']:
                stmt += '\n' + f"{booking[1]} {booking[0][5:]} {booking[2][:5]} - {booking[3][:5]}"
            stmt += "\n\n*NORMAL TABLE*"
            for booking in bookings['normal']:
                stmt += '\n' + f"{booking[1]} {booking[0][5:]} {booking[2][:5]} - {booking[3][:5]}"
            stmt += "\n\n*OTHER NORMAL TABLE*"
            for booking in bookings['other']:
                stmt += '\n' + f"{booking[1]} {booking[0][5:]} {booking[2][:5]} - {booking[3][:5]}"
        update.message.reply_text(parse_mode='Markdown', text=stmt)
    except:
        update.message.reply_text('error')

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