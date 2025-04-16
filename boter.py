from pyrogram import Client, filters
from PIL import Image, ImageFilter
import io
import os

# زانیاری بۆت لێرە دانێ
api_id = 16871970  # گۆڕە بە api_id خۆت
api_hash = "5f3cf7cb43fa552e8136555a5155a9c8"  # api_hash
bot_token = "7910838916:AAHOauvJduFaQKF5nVBJhMxFOBRuV71oGMA"  # token لە BotFather وەربگرە

app = Client("image_cleaner_bot",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)


# فرمانی /start
@app.on_message(filters.command("start"))
async def start_handler(client, message):
  await message.reply_text(
      "سڵاو! من بوتێکم بۆ سافکردنی وێنەکان. تکایە وێنە بنێرە!")


# وەرگرتنی وێنە و چاککردنی
@app.on_message(filters.photo)
async def photo_handler(client, message):
  await message.reply_text("وێنەکەت وەرگیرا... ساف دەکەم!")

  # داگرتنی فایلەکە
  file_path = await message.download()

  try:
    # کرتەکردنەوەی وێنە
    img = Image.open(file_path)

    # فلتەرکردن
    filtered_img = img.filter(ImageFilter.DETAIL)

    # گەڕاندنەوە بۆ بایتس بۆ ناردن
    output = io.BytesIO()
    output.name = "cleaned.jpg"
    filtered_img.save(output, format="JPEG")
    output.seek(0)

    # ناردنی وێنەی سافکراو
    await message.reply_photo(photo=output, caption="ئەمە وێنەی سافکراوە!")

  except Exception as e:
    await message.reply_text(f"هەڵەیەک ڕوویدا: {e}")

  finally:
    if os.path.exists(file_path):
      os.remove(file_path)


app.run()