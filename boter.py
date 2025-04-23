from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import numpy as np

# Custom Lightroom-style filter
def apply_custom_filter(img: Image.Image) -> Image.Image:
    # Exposure +0.75
    img = ImageEnhance.Brightness(img).enhance(1.75)

    # Contrast -30
    img = ImageEnhance.Contrast(img).enhance(0.7)

    # Saturation +20
    img = ImageEnhance.Color(img).enhance(1.2)

    # Sharpness / Clarity +15
    img = ImageEnhance.Sharpness(img).enhance(2.0)

    # Highlights, Shadows, Whites, Blacks simulated (basic method)
    arr = np.array(img).astype(np.int16)
    arr = arr + 3  # Shadows +3
    arr = np.clip(arr, 0, 255)

    img = Image.fromarray(arr.astype(np.uint8))

    # Grain +5
    noise = np.random.normal(0, 5, arr.shape).astype(np.uint8)
    grainy = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(grainy)

    return img

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! وێنە بنێرە بۆ فلتەرکراوی بە شێوازی Lightroom.")

# Handle photo
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        image_bytes = await file.download_as_bytearray()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        filtered = apply_custom_filter(image)

        output = BytesIO()
        filtered.save(output, format="JPEG")
        output.seek(0)

        await update.message.reply_photo(photo=output, caption="وێنەکەت بە فلتەری تایبەتی سەرەکی فلتەر کرا!")

    except Exception as e:
        await update.message.reply_text(f"هەڵەیەک ڕوویدا: {e}")

# Run bot
def main():
    app = Application.builder().token("7889615610:AAGhVmzVmGSuE7RkPmfWwjCFoWspRug_ZP4").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
