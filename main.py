import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from rembg import remove

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Do NOT hardcode your token

os.makedirs("images", exist_ok=True)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = f"images/{photo.file_unique_id}.png"
    await file.download_to_drive(file_path)

    await update.message.reply_text("Removing background...")

    with open(file_path, "rb") as i:
        input_data = i.read()
        output_data = remove(input_data)

    output_path = file_path.replace(".png", "_no_bg.png")
    with open(output_path, "wb") as o:
        o.write(output_data)

    await update.message.reply_photo(photo=InputFile(output_path))

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot is running...")
    app.run_polling()
