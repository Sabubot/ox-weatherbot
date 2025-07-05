
import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

ROUTES = {
    "tbilisi": "Tbilisi,GE",
    "batumi": "Batumi,GE",
    "kutaisi": "Kutaisi,GE",
    "gori": "Gori,GE",
    "telavi": "Telavi,GE"
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_weather(city: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "main" not in data:
        return "❌ Unable to get weather data."

    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    wind = data["wind"]["speed"]

    return (
        f"🌤️ Weather in {city}:\n"
        f"📌 {weather.capitalize()}\n"
        f"🌡️ Temperature: {temp}°C (Feels like {feels}°C)\n"
        f"💨 Wind Speed: {wind} m/s"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    route_list = '\n'.join([f"/{cmd}" for cmd in ROUTES])
    await update.message.reply_text(f"🌤️ Welcome to OX_Weatherbot!\n\nUse commands to get weather:\n{route_list}")

def create_route_handler(city_name: str):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        report = get_weather(city_name)
        await update.message.reply_text(report)
    return handler

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    for cmd, city in ROUTES.items():
        app.add_handler(CommandHandler(cmd, create_route_handler(city)))

    print("✅ OX_Weatherbot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
