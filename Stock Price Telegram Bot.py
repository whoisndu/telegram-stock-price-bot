# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:18:27 2023

@author: NDU-PC
"""

import os
import time
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

# Load environment variables from .env file
load_dotenv()

# Telegram bot token
TOKEN = "YOUR_TELEGRAM_KEY"

# Function to get stock price for a given ticker
def get_stock_price(ticker):
    url = f"https://api.marketstack.com/v1/tickers/{ticker}/intraday/latest"
    params = {
        'access_key': os.getenv("YOUR_MARKET_STACK_ACCESS_KEY")
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'data' in data:
        return data['data']['last']
    return None

# Function to send stock price updates to Telegram
def send_stock_updates(context):
    job = context.job
    chat_id = job.context['chat_id']
    tickers = job.context['tickers']
    for ticker in tickers:
        price = get_stock_price(ticker)
        if price is not None:
            if 'last_price' in job.context:
                prev_price = job.context['last_price'].get(ticker)
                if prev_price is not None:
                    percentage_change = ((price - prev_price) / prev_price) * 100
                    context.bot.send_message(chat_id=chat_id, text=f"{ticker}: {price:.2f} ({percentage_change:.2f}%)")
            job.context['last_price'][ticker] = price

# Function to start the bot
def start(update, context):
    chat_id = update.effective_chat.id
    if len(context.args) < 1:
        update.message.reply_text("Please provide the list of stock tickers as command arguments.Example: /start AAPL GOOG")
        return

    tickers = context.args
    context.job_queue.run_repeating(send_stock_updates, interval=43200, first=0,
                                    context={'chat_id': chat_id, 'tickers': tickers, 'last_price': {}})
    update.message.reply_text("Stock price updates enabled!")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
