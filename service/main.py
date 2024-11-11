import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Define the folder where images will be saved
SAVE_FOLDER = "/app/images"  # This will be mounted to a host folder in Docker

# Ensure the save folder exists
os.makedirs(SAVE_FOLDER, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me an image, and I will save it.")

async def save_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        # Get the highest quality photo from the message
        photo = update.message.photo[-1]
        # Download the photo to the specified folder
        file_path = os.path.join(SAVE_FOLDER, f"{photo.file_unique_id}.jpg")
        await photo.get_file().download(file_path)
        await update.message.reply_text("Image saved successfully!")

def main():
    bot_token = os.getenv("BOT_TOKEN")  # Token from environment variable
    application = ApplicationBuilder().token(bot_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, save_image))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
