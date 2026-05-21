import os
import telebot
import yt_dlp

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8935065883:AAGvYcaXUVeaXwDM03RjeMJj1d_Vtmx9AdQ"

bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# ---------- START MENU ----------
@bot.message_handler(commands=['start'])
def start(message):

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("📺 YouTube", callback_data="youtube"),
        InlineKeyboardButton("🎵 TikTok", callback_data="tiktok"),
        InlineKeyboardButton("📘 Facebook", callback_data="facebook"),
        InlineKeyboardButton("📸 Instagram", callback_data="instagram"),
        InlineKeyboardButton("📌 Pinterest", callback_data="pinterest"),
    )

    bot.send_message(
        message.chat.id,
        "🔥 আপনি কি ভিডিও ডাউনলোড দিবেন সেটি নির্বাচন করুন 👇",
        reply_markup=markup
    )


# ---------- BUTTON HANDLER ----------
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    data = call.data

    text_map = {
        "youtube": "📺 YouTube লিংক পাঠান",
        "tiktok": "🎵 TikTok লিংক পাঠান",
        "facebook": "📘 Facebook লিংক পাঠান",
        "instagram": "📸 Instagram লিংক পাঠান",
        "pinterest": "📌 Pinterest লিংক পাঠান",
    }

    if data in text_map:
        bot.send_message(call.message.chat.id, text_map[data])


# ---------- DOWNLOAD HANDLER ----------
@bot.message_handler(func=lambda message: message.text and message.text.startswith("http"))
def download_video(message):

    url = message.text

    msg = bot.reply_to(message, "📥 ভিডিও ডাউনলোড হচ্ছে...")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, "rb") as video:
            bot.send_video(message.chat.id, video, caption="✅ ডাউনলোড সম্পন্ন")

        os.remove(file_path)

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Error:\n{e}",
            message.chat.id,
            msg.message_id
        )


print("🔥 Bot Running...")
bot.infinity_polling()
