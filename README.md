# ssl-certificate-checker-py

# Intro

This module was created to check SSL certificates at a given URL and notify you in Telegram

# Requirements

In this module, the following libraries were used:
```
from datetime import datetime, timedelta
from os import environ
from ssl import get_server_certificate
from urllib.parse import urlparse
from logging import error, basicConfig, INFO, info

from cryptography import x509
from cryptography.hazmat.backends import default_backend

import telebot
from telebot.types import Message
```
You also need to find a bot in the Telegram named **[SSL Certificate Checker](https://t.me/SSL_Certificate_CheckerBot)**

