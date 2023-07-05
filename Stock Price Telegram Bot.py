# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 14:51:59 2023

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
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Function to get stock price for a given ticker
def get_stock_price(ticker):
    url = f"https://api.marketstack.com/v1/tickers/{ticker}/intraday/latest"
    params = {"access_key": os.getenv("MARKETSTACK_API_KEY")}
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data:
        return data["data"]["last"]
    return None


# Function to send stock price updates to Telegram
def send_stock_updates(context):
    chat_id = context.job.context
    tickers = context.job.context["tickers"]
    for ticker in tickers:
        price = get_stock_price(ticker)
        if price is not None:
            if "last_price" in context.chat_data:
                prev_price = context.chat_data["last_price"].get(ticker)
                if prev_price is not None:
                    percentage_change = (
                        (price - prev_price) / prev_price
                    ) * 100
                    context.bot.send_message(
                        chat_id=chat_id,
                        text=f"{ticker}: {price:.2f} ({percentage_change:.2f}%)",
                    )
            context.chat_data["last_price"][ticker] = price


# Function to start the bot
def start(update, context):
    chat_id = update.effective_chat.id
    if len(context.args) < 1:
        update.message.reply_text(
            "Please provide the list of stock tickers as command arguments."
        )
        return

    tickers = context.args
    context.chat_data["tickers"] = tickers
    context.chat_data["last_price"] = {}
    job_queue = context.job_queue
    job_queue.run_repeating(
        send_stock_updates, interval=43200, first=0, context=context
    )  # Send updates twice a day (every 12 hours)
    update.message.reply_text("Stock price updates enabled!")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
