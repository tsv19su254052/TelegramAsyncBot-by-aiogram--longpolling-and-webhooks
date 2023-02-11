# Interpreter 3.10

import asyncio
import sys
import os
from aiogram import Bot, Dispatcher, types
import configparser

from bot import db, filters, handlers, middlewares
#from bot.config import USE_WEBHOOK, WEBHOOK_SERVER, WEBHOOK_URL, SSL_CERT
from bot.config import WEBHOOK_SERVER, SSL_CERT
from bot.misc import executor


# todo Переделать конфигу с *.py на *.ini - СДЕЛАЛ
# todo Изучить библиотеки:
#  - json-configparser,
#  - yaml-config-parser,
#  - yaml-config-reader,
#  - yaml-config,
#  - yaml-configuration - пока не ставятся
current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)


async def on_startup_polling(dp: Dispatcher):
    await dp.bot.delete_webhook()


async def on_startup_webhook(dp: Dispatcher):
    # todo Сделать открытие и чтение сертификата с USB-вого токена
    # fixme Переместить внутрь обработки исключения
    cert = open(SSL_CERT, 'rb') if SSL_CERT else None
    #await dp.bot.set_webhook(WEBHOOK_URL, certificate=cert)
    await dp.bot.set_webhook(config.get("Web-Hook", "webhook-url"), certificate=cert)


async def on_shutdown_webhook(dp: Dispatcher):
    await dp.bot.delete_webhook()


def main():
    executor.on_startup(on_startup_polling, webhook=0)
    executor.on_startup(on_startup_webhook, polling=0)
    executor.on_shutdown(on_shutdown_webhook, polling=0)
    # if USE_WEBHOOK:
    #     executor.start_webhook(**WEBHOOK_SERVER)
    # else:
    #     executor.start_polling()
    if config.getboolean("Tech", "use-webhook"):
        executor.start_webhook(config.get("Web-Hook", "webhook-server"))
    else:
        executor.start_polling()


if __name__ == '__main__':
    main()
