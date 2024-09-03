import os
import sys

from config import *
from configparser import ConfigParser

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
        save(l_config)
        sys.exit()

    return l_config
