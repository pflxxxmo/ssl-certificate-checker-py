import ssl
import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta
from urllib.parse import urlparse
import telebot

# access token for telegram bot
access_token = os.environ.get('API_KEY')
# the time to notify of the expiration of the certificate(days)
notice_date = 10
bot = telebot.TeleBot(access_token)


def check_certificate(url: str):
    parsed_url = urlparse(url)
    try:
        cert = ssl.get_server_certificate(
            (parsed_url.hostname, parsed_url.port or 443))
    except Exception:
        return "Bad request"
    try:
        parsed_cert = x509.load_pem_x509_certificate(str.encode(cert), default_backend())
    except Exception:
        return
    date = parsed_cert.not_valid_after
    if date < datetime.today() or (date - datetime.today()) <= timedelta(notice_date):
        return f'ALARM‼️. The certificate for url {url} was expired in {date}'
    else:
        return f'OK🆗.The certificate for url {url} expires in {date}'


@bot.message_handler(content_types=['text'])
def response(message):
    if str(message.text).startswith("https://"):
        url = message.text
        bot.send_message(message.chat.id, check_certificate(url))
    else:
        url = "https://" + message.text
        bot.send_message(message.chat.id, check_certificate(url))


bot.polling(none_stop=True)
