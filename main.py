import os
import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import requests

# Initialize Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your Telegram Bot API token
TELEGRAM_BOT_TOKEN = '6304259542:AAGLVkd4Ku8mnwquC9qwR8p_D2Wf9R2O-nA'

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me any social media link and I will download the media for you!')

# Media Downloader using yt-dlp (YouTube, Instagram, TikTok, Twitter, etc.)
def download_media(link: str) -> str:
    output_path = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Options for yt-dlp to download media
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'noplaylist': True,
        'format': 'best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        file_path = ydl.prepare_filename(info)
    
    return file_path

# Handling media download requests
def handle_media(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    user = update.message.from_user
    logger.info(f"User {user.first_name} sent a link: {message}")

    # Validate the message content
    if not message.startswith("http"):
        update.message.reply_text("Please send a valid URL.")
        return

    try:
        # Download the media
        update.message.reply_text("Downloading your media, please wait...")
        file_path = download_media(message)
        # Send the downloaded file to the user
        with open(file_path, 'rb') as file:
            update.message.reply_document(file)
        os.remove(file_path)
    except Exception as e:
        logger.error(f"Error downloading media: {str(e)}")
        update.message.reply_text("Failed to download media. Please check the URL or try again later.")

# Error handler
def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    update.message.reply_text("An error occurred. Please try again later.")

# Main Function to run the bot
def main() -> None:
    # Set up the Updater and Dispatcher
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_media))
    dispatcher.add_error_handler(error_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
