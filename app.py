import os
from telegram import Update
from telegram.ext import Application, CommandHandler
import requests
import pandas as pd
import matplotlib.pyplot as plt

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, _):
    await update.message.reply_text("""
    سڵاو! 👋 بۆتی نرخی زێڕم.
    فەرمانەکان:
    /price - نرخی ئێستا
    /chart - گرافیکی نرخ
    """)

async def get_price(update: Update, _):
    price = requests.get("https://api.metals.live/v1/spot/XAUUSD").json()["price"]
    await update.message.reply_text(f"🏆 نرخی زێڕ: {price:.2f} USD")

async def plot_chart(update: Update, _):
    data = pd.DataFrame({'price': [requests.get("https://api.metals.live/v1/spot/XAUUSD").json()["price"] for _ in range(10)]})
    plt.plot(data['price'])
    plt.savefig('chart.png')
    await update.message.reply_photo(photo=open('chart.png', 'rb'))

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", get_price))
app.add_handler(CommandHandler("chart", plot_chart))
app.run_polling()
