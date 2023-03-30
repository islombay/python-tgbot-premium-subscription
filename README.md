# Telegram bot with premium subscription

**Notice:** Premium is not official telegram messanger's premium subscription

## What is this bot about

This is a test bot with some functionality in buying coins using telegram methods of payment. Database (mongodb) exists.

<hr>
<br>

## Quick start

First of all, download all modules that you need to run the bot. Use the command below:

```
pip install requirements
```

Next, create your own telegram bot using [BotFather](https://telegram.me/botFather) (hope everyone knows how to do that). Once you get a bot token, change the value for `BOT_TOKEN` in `.env` file using your own one.
Do not forget to set your telegram accounts id for `DEV_ADMIN` in the same file. This is needed for notifing you when bot is started.

### Database - MongoDB

Install it

### **Run the bot**

Following command starts the bot:

```
python3 main.py
```
