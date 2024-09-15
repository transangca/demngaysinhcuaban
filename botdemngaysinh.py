import telebot
import requests

# Thay thế 'YOUR_TELEGRAM_BOT_TOKEN' bằng token của bạn
TOKEN = '6380919096:AAGcL0HmiJ2ynJaHoGj-4sOLgquQS6g9208'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Xin chào! Gửi cho gửi cho tao cái ngày sinh địa chỉ exampp: /sinhngay 10/9/2007')

@bot.message_handler(commands=['sinhngay'])
def get_date_info(message):
    # Tách ngày từ tin nhắn
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Gửi cho tao cái ngày sinh địa chỉ exampp: /sinhngay 10/9/2007')
        return

    date = message.text.split(maxsplit=1)[1]
    try:
        response = requests.get(f'https://api.sumiproject.net/date?date={date}')
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        data = response.json()

        # Xử lý dữ liệu theo cấu trúc đã cung cấp
        if 'years' in data:
            details = (
                f"Thông tin ngày:\n"
                f"Năm: {data.get('years', 'N/A')}\n"
                f"Tháng: {data.get('months', 'N/A')}\n"
                f"Tuần: {data.get('weeks', 'N/A')}\n"
                f"Ngày: {data.get('days', 'N/A')}\n"
                f"Giờ: {data.get('hours', 'N/A')}\n"
                f"Phút: {data.get('minutes', 'N/A')}\n"
                f"Giây: {data.get('seconds', 'N/A')}\n"
            )
            bot.reply_to(message, details)
        else:
            bot.reply_to(message, 'No data found for this date.')

    except requests.RequestException as e:
        bot.reply_to(message, f'An error occurred: {e}')

if __name__ == '__main__':
    bot.polling()
