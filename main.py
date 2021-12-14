import ssl
from time import time
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
import telebot

# access token for telegram bot
access_token = '5035846405:AAHJQ_--GbDeF8DXDe827gRFoflNe_xA75o'
# the time to notify of the expiration of the certificate   
notice_date = 432000
bot = telebot.TeleBot(access_token)


def check_certificate(url):
    parsed_url = urlparse(url)
    try:
        cert = ssl.get_server_certificate(
            (parsed_url.hostname, parsed_url.port or 443))
    except Exception:
        return "Bad request"
    # save cert to temporary file (filename required for _test_decode_cert())
    temp_filename = Path(__file__).parent / "temp.crt"
    with open(temp_filename, "w") as f:
        f.write(cert)
    try:
        parsed_cert = ssl._ssl._test_decode_cert(temp_filename)
    except Exception:
        return
    finally:  # delete temporary file
        temp_filename.unlink()
    date = ssl.cert_time_to_seconds(parsed_cert["notAfter"])
    if date < time() or (date - time()) <= notice_date:
        return f'ALARM‼️. The certificate for url {url} was expired in {datetime.utcfromtimestamp(date).strftime("%b %d %Y %Z")}'
    else:
        return f'OK🆗.The certificate for url {url} expires in {datetime.utcfromtimestamp(date).strftime("%b %d %Y %Z")}'


@bot.message_handler(content_types=['text'])
def response(message):
    if str(message.text).startswith("https://"):
        url = message.text
        bot.send_message(message.chat.id, check_certificate(url))
    else:
        url = "https://" + message.text
        bot.send_message(message.chat.id, check_certificate(url))


bot.polling(none_stop=True)
