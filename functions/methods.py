from functions import init

config = init.config()


def get_chats(socnet: str):
    if not config['GENERAL']['{}_FORWARD_IDES'.format(socnet.upper())]:
        return []
    return config['GENERAL']['{}_FORWARD_IDES'.format(socnet.upper())].split(' ')
