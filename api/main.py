from fastapi import FastAPI
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


app = FastAPI()

@app.get("/")
async def health_check():
    return "The health check is successful"
BOT_TOKEN = os.getenv("8113117364:AAEBZZZQrX2RfmvrKcNfntkvIsgnt-OrTw")
bot = AsyncTeleBot(BOT_TOKEN)
