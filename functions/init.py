import os
import sys

from config import *
from configparser import ConfigParser
from pyrogram import Client, types
from pyrogram.errors import exceptions

os.makedirs(sessions_path, exist_ok=True)


def config():
    exists = os.path.exists(config_path)

    def save(x):
        x.write(open(config_path, 'w', encoding=encoding))

    if not exists:
        open(config_path, 'w', encoding=encoding).write('')

    l_config = ConfigParser()
    l_config.read(config_path, encoding=encoding)

    if not exists:
        print(t_config_first)
        l_config.add_section('GENERAL')
        l_config['GENERAL']['API_ID'] = input('API_ID: ')
        l_config['GENERAL']['API_HASH'] = input('API_HASH: ')
        l_config['GENERAL']['CHANNEL_CHECK'] = input('Канал отслеживания (Телеграм): ')
        save(l_config)
        sys.exit()

    return l_config


def client():
    l_config = config()
    app = Client(tg_sess_path.rpartition('.')[0], api_id=l_config['GENERAL']['API_ID'],
                 api_hash=l_config['GENERAL']['API_HASH'])
    if os.path.exists(tg_sess_path):
        return app

    app.connect()

    while True:
        phone_number = input("Введите ваш номер телефона: ")
        try:
            sent_code_info = app.send_code(phone_number)
            break
        except exceptions.PhoneNumberInvalid:
            print('Номер телефона неверный! Попробуйте ещё раз!')

    phone_code = input("Код был выслан. Введите его, пожалуйста: ")
    while True:
        try:
            app.sign_in(phone_number, sent_code_info.phone_code_hash, phone_code)
            break

        except exceptions.PhoneNumberInvalid:
            print('Код неправильный!')
            phone_code = input("Введите код: ")

        except exceptions.SessionPasswordNeeded:
            password = input("У вас стоит пароль. Введите его: ")
            while True:
                try:
                    app.check_password(password)
                    break
                except exceptions.PasswordHashInvalid:
                    print('Пароль неверный!')
                    password = input("Введите пароль: ")

    app.disconnect()

    return app

