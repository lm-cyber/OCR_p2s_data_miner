import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from aiobotocore.session import get_session
from botocore.exceptions import ClientError

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "images")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "test_out")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "test_out")

async def get_minio_client():
    session = get_session()
    client = session.create_client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        region_name="us-east-1",
    )
    return client

async def ensure_bucket_exists(client):
    try:
        response = await client.list_buckets()
        bucket_names = [bucket["Name"] for bucket in response["Buckets"]]

        if MINIO_BUCKET_NAME not in bucket_names:
            await client.create_bucket(Bucket=MINIO_BUCKET_NAME)
    except ClientError as e:
        print(f"An error occurred: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me an image, and I'll save it to MinIO.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Download the image
    photo = update.message.photo[-1]  # Get the highest resolution
    file = await photo.get_file()
    file_path = f"{update.message.from_user.id}/{photo.file_unique_id}.jpg"

    # Save the file to MinIO
    async with get_minio_client() as client:
        await ensure_bucket_exists(client)

        # Download the file to a temporary location
        local_path = f"/tmp/{file_path}"
        await file.download_to_drive(local_path)

        # Upload to MinIO
        try:
            with open(local_path, "rb") as data:
                await client.put_object(Bucket=MINIO_BUCKET_NAME, Key=file_path, Body=data)
            await update.message.reply_text(f"Image saved as {file_path} in MinIO!")
        except ClientError as e:
            await update.message.reply_text("Failed to upload image.")
            print(f"An error occurred: {e}")

async def main():
    # Create the application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Initialize the application explicitly
    await application.initialize()  # Explicit initialization step

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Start the bot
    await application.start()
    await application.idle()

if __name__ == "__main__":
    asyncio.run(main())
