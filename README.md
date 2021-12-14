# ssl-certificate-checker-py

# Intro

This module was created to check SSL certificates at a given URL and notify you in Telegram

# Requirements

In this module, the following libraries were used:
```
import ssl
from time import time
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
import telebot
```
You also need to find a bot in the Telegram named **[SSL Certificate Checker](https://t.me/SSL_Certificate_CheckerBot)**

