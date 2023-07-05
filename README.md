# telegram-stock-price-bot
**Telegram Stock Price Update Bot**

This Telegram bot allows users to receive stock price updates for their desired list of stock tickers. The bot sends updates twice a day, providing information about the opening and closing prices of the specified stocks, along with the percentage rise or fall in the stock price since the last update.

**Prerequisites**
Before using the bot, make sure you have the following:
1. Python 3 installed on your machine
2. Telegram bot token obtained from the BotFather on Telegram
3. MarketStack API key for fetching stock price data
   
**Setup**
1. Clone this repository to your local machine or download the script file.
2. Install the required packages by running the following command:
```
pip install python-telegram-bot python-dotenv requests
```
3. Obtain a Telegram bot token by following the steps below:
4. Create a new bot on Telegram by talking to the BotFather - https://core.telegram.org/bots#3-how-do-i-create-a-bot
5. Save the bot token.
6. Obtain an API key from the MarketStack API by following the steps below:
- Sign up for a free account on the MarketStack website - https://marketstack.com/.
- Retrieve your API key from your MarketStack account dashboard.
- Save the API key.

**Configuration**
1. Create a new file in the project directory called .env.
2. Open the .env file and add the following lines:
```
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
MARKETSTACK_API_KEY=YOUR_MARKETSTACK_API_KEY
```
3. Replace YOUR_TELEGRAM_BOT_TOKEN with the Telegram bot token you obtained.
4. Replace YOUR_MARKETSTACK_API_KEY with the MarketStack API key you obtained.

**Usage**
1. Open a terminal or command prompt and navigate to the project directory.
2. Run the Python script using the following command:
```python stock_price_bot.py```
3. Start a chat with your Telegram bot.

In the chat, send the /start command followed by the desired stock tickers as command arguments. For example: /start AAPL GOOGL MSFT. Make sure to separate each ticker with a space.
The bot will now send you stock price updates twice a day (at the opening and closing prices) for the specified tickers, along with the percentage rise or fall in the stock price since the last update.

**Customization**
To modify the list of stock tickers, open the Python script and update the tickers list with your desired tickers.
You can customize the interval between updates by modifying the interval parameter in the ```job_queue.run_repeating``` function call in the ```send_stock_updates``` function.
Feel free to enhance the bot's functionality or add additional features as per your requirements.
