# 📄 Paperless Telegram Bot

Telegram bot to interact with your Paperless-ngx instance, allowing you to send documents directly from Telegram.
## 💖 Support

If you find this project useful, consider supporting its development:

[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue.svg?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=FTZWS9USG8GB4)
## 🌟 Features

- 📤 **Document upload**: Upload documents to Paperless-ngx directly from Telegram
- 📎 **Multiple formats**: Compatible with PDF and images
- 🏷️ **Tag management**: Add tags and categories to your documents
- 📋 **Interactive menus**: Intuitive interface with buttons and menus
- 🌐 **Multi-language**: Support for multiple languages through localization files
- 🔒 **Secure**: Authentication with your Paperless-ngx instance, and allows connections only from authorized Telegram users

## 📋 Requirements

- Python 3.8 or higher
- A running instance of [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)
- A Telegram bot (token from BotFather)
- Python dependencies (see below)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/TamuAlex/paperless-telegram-bot.git
cd paperless-telegram-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a Telegram bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send the command `/newbot`
3. Follow the instructions to create your bot
4. Save the **API token** provided by BotFather

### 4. Get your User ID

1. Send a message to @userid4Bot on Telegram to get your userID

### 5. Configure the bot

Edit the `config.yaml` file with your data.

### 6. Get your Paperless API Token

More information at the following link: https://docs.paperless-ngx.com/api/

## 🎮 Usage

### Start the bot

```bash
python telegramBot.py
```

The bot will start and be ready to receive commands.

### Available commands

- `/hello` - Test if the bot is operational with a response message

### Typical workflow

1. **Send a document or photo** to the bot
2. The bot will ask if you want to add:
   - Custom title
   - Tags
   - Correspondent
   - Document type
3. Confirm and the document will be uploaded to Paperless-ngx



## 📁 Project structure

```
paperless-telegram-bot/
├── telegramBot.py       # Main bot script
├── telegramMenus.py     # Menu and keyboard definitions
├── utils.py             # Helper functions
├── config.yaml          # Configuration file
├── requirements.txt     # Requirements file
├── locales/             # Translation files
│   ├── es.yaml
│   ├── en.yaml
│   └── ...
└── README.md            # This file
```
