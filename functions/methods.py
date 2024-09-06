from functions import init

config = init.config()


def get_chats(socnet: str):
    if not config['GENERAL']['VK_FORWARD_IDES']:
        return []
    return config['GENERAL']['{}_FORWARD_IDES'.format(socnet.upper())].split(' ')
