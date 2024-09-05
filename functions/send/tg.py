import os
import time
from functions import *
from vk_api import VkUpload
from config import *

config = init.config()


async def upload_photo(client, message):
    path_temp_photo = os.path.join(temp_path, f'{time.time()}.jpg')
    await client.download_media(message.photo.file_id,
                                file_name=path_temp_photo)

    return path_temp_photo.replace('\\', '/')


async def photo(client, message):
    for tg_chat_id in config['GENERAL']['TG_PASSWORD_IDES'].split(' '):
        await client.send_photo(tg_chat_id.replace('https://t.me/', ''),
                                photo=(ptp := (await upload_photo(client, message))),
                                caption=message.caption)
        os.remove(ptp)


async def upload_video(client, message):
    path_temp_video = os.path.join(temp_path, f'{time.time()}.mp4')
    await client.download_media(message.video.file_id,
                                file_name=path_temp_video)
    return path_temp_video


async def video(client, message):
    for tg_chat_id in config['GENERAL']['TG_PASSWORD_IDES'].split(' '):
        await client.send_video(tg_chat_id.replace('https://t.me/', ''),
                                video=(ptp := (await upload_video(client, message))),
                                caption=message.caption)
        os.remove(ptp)
