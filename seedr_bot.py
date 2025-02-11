import os
import requests
from tqdm import tqdm
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token from BotFather
BOT_TOKEN = "7250466326:AAFJ3oUCNyglFpkq75OxGlxB8SesPkQDPgc"

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a Seedr.cc download link, and I'll download the file for you.")

# Function to handle Seedr.cc download links
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    try:
        # Send a message to indicate the download has started
        await update.message.reply_text("Starting download...")

        # Download the file with progress
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = url.split("/")[-1]  # Extract file name from the URL
            total_size = int(response.headers.get("content-length", 0))  # Get total file size

            # Initialize the progress bar
            progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc=file_name)

            # Download the file in chunks
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        progress_bar.update(len(chunk))  # Update the progress bar

            progress_bar.close()  # Close the progress bar

            # Send the file back to the user
            await update.message.reply_document(document=open(file_name, "rb"))
            os.remove(file_name)  # Clean up the file after sending
        else:
            await update.message.reply_text("Failed to download the file. Please check the link.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function to run the bot
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    # Start the bot
    print("Bot is running...")
    app.run_polling()
