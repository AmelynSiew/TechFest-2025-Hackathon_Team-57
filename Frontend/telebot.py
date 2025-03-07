from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline

# Load the misinformation detection model
misinformation_detector = pipeline("text-classification", model="facebook/bart-large-mnli")

# Replace with your Telegram bot token
BOT_TOKEN = "8123283154:AAEun9YLdCc--enHywJMNgTu1M85HO6IS5Q"

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🚀 Welcome to the Misinformation Detection Bot!
Paste any text, and I'll analyze it for potential misinformation.
""")

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # Analyze the text
    result = misinformation_detector(user_input)

    # Prepare the response
    response = (
        f"**Analysis Result:**\n"
        f"Label: {result[0]['label']}\n"
        f"Confidence: {result[0]['score']:.2f}\n\n"
    )
    if result[0]['label'] == "misinformation":
        response += "⚠️ This text is likely to contain misinformation."
    else:
        response += "✅ This text seems reliable."

    # Send the response back to the user
    await update.message.reply_text(response)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Main function to run the bot
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    # Start the bot
    print("Polling...")
    app.run_polling(poll_interval=3)