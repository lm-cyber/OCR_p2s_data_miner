import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import uuid
# Define the folder where images will be saved
SAVE_FOLDER = "/app/images"  # This will be mounted to a host folder in Docker

# Ensure the save folder exists
os.makedirs(SAVE_FOLDER, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me an image, and I will save it.")
async def save_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    file = update.message.photo[-1].file_id
    obj = await context.bot.get_file(file)
    file_path = os.path.join(SAVE_FOLDER, f"{uuid.uuid4()}.jpg")

    await obj.download_to_drive(file_path)

    # await file.download_to_drive(SAVE_FOLDER)
    # if update.message.photo:
    #     # Get the highest quality photo from the message
    #     file = await update.message.photo[-1].get_file()
    #     print(type(file),file)
        # # First, await photo.get_file() to retrieve the file
        # file_path = os.path.join(SAVE_FOLDER, f"{photo}.jpg")

        # file = await photo.download(file_path)

        # Now download the file
        # await file.download(file_path)
        # await update.message.reply_text("Image saved successfully!")


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
