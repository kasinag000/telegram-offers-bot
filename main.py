import os
import json
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator
from dotenv import load_dotenv

# Load .env secrets
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USERS = os.getenv("ALLOWED_USERS", "").split(",")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load translator
translator = Translator()

# Store search history
HISTORY_FILE = "user_data.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

# Dummy message pool
DUMMY_MESSAGES = [
    "Great deal on AC at ₹25,999 – Free delivery!",
    "Samsung 1.5 Ton AC available at lowest price!",
    "Exchange offer: Buy AC and get ₹3000 cashback!"
]

# Handle start/hi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return
    await update.message.reply_text("Hi! Please enter a keyword to search offers:")

# Handle messages (keywords)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Access denied.")
        return

    keyword = update.message.text.strip()
    dummy_results = random.sample(DUMMY_MESSAGES, k=min(2, len(DUMMY_MESSAGES)))

    combined = "\n".join(dummy_results)
    telugu_summary = translator.translate(combined, dest='te').text

    response = f"🔍 Results for: *{keyword}*\n\n{combined}\
