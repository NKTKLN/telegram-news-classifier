from bot.telegram_bot import TelegramBot

bot = TelegramBot()
bot.client.run_until_disconnected()
