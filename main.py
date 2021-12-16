from datetime import datetime, timedelta
from os import environ
from ssl import get_server_certificate
from urllib.parse import urlparse
from logging import error, basicConfig, INFO, info

from cryptography import x509
from cryptography.hazmat.backends import default_backend

import telebot
from telebot.types import Message

# access token for telegram bot
access_token = environ.get('API_KEY')
# the time to notify of the expiration of the certificate(days)
notice_date = 10
bot = telebot.TeleBot(access_token)


def check_certificate(url: str) -> tuple:
    """Takes one parameter of type string, returns a tuple with values of type bool and datetime.datetime.
    This function parses and decrypts PEM certificate."""

    parsed_url = urlparse(url)
    try:
        cert = get_server_certificate(
            (parsed_url.hostname, parsed_url.port or 443))
    except:
        error('Name or service not known. Status: ERROR')
        return None, False
    parsed_cert = x509.load_pem_x509_certificate(
        str.encode(cert), default_backend())
    info(f'The certificate for the URL has been received:{url}. Status: INFO')
    if parsed_cert.not_valid_after < datetime.today() or (parsed_cert.not_valid_after - datetime.today()) <= timedelta(notice_date):
        return parsed_cert.not_valid_after, True
    else:
        return parsed_cert.not_valid_after, False


def prepare_for_response(url: str) -> str:
    """The function takes a value of type str and returns a value of type str. 
    This function takes an address, sends it for checking and as a result gives a string for the answer. """

    date, result = check_certificate(url)
    if date == None and result == False:
        return 'The certificate at this URL does not exist'
    else:
        if result:
            return f'ALARM‼️. The certificate for url {url} was expired in {date}'
        else:
            return f'OK🆗.The certificate for url {url} expires in {date}'


@bot.message_handler(content_types=['text'])
def response(message: Message):
    """The function takes a message of type telebot.Message.
    This function is responsible for finding the string entered by the bot and sending it for processing.
    This function also allows the bot to send a message with the result of processing"""

    if str(message.text).startswith("https://"):
        url = message.text
        bot.send_message(message.chat.id, prepare_for_response(url))
    else:
        url = "https://" + message.text
        bot.send_message(message.chat.id, prepare_for_response(url))


basicConfig(format='%(asctime)s - %(message)s', level=INFO)
bot.polling(none_stop=True)
