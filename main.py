import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

def parse_amount(amount_str):
    amount_str = amount_str.lower()

    if 'k' in amount_str:
        base = int(amount_str.replace('k', '')) * 1000
    else:
        base = int(amount_str)

    return base * 1000

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    match = re.match(r'^(M|K)\s+(\d+k?|\d+)\s+(.+)', text, re.IGNORECASE)
    if not match:
        return

    type_, amount, desc = match.groups()
    value = parse_amount(amount)

    if type_.upper() == 'M':
        result = f"lapor pemasukan {value} {desc}"
    else:
        result = f"lapor pengeluaran {value} {desc}"

    await update.message.reply_text(result)

app = ApplicationBuilder().token(os.getenv("8674749505:AAHhaEcfe3e4rD349oqIMG0CwT5Z7y0H3eA")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
