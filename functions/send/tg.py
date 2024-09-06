import os
import time
from functions import *
from vk_api import VkUpload
from config import *
from pyrogram import types, Client

config = init.config()


async def upload_photo(client, message):
    path_temp_photo = os.path.join(temp_path, f'{time.time()}.jpg')
    await client.download_media(message.photo.file_id,
                                file_name=path_temp_photo)

    return path_temp_photo.replace('\\', '/')


async def photo(client, message):
    for tg_chat_id in methods.get_chats('tg'):
        print('dsa')
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
    for tg_chat_id in methods.get_chats('tg'):
        await client.send_video(tg_chat_id.replace('https://t.me/', ''),
                                video=(ptp := (await upload_video(client, message))),
                                caption=message.caption)
        os.remove(ptp)


async def poll(client: Client, message: types.Message):
    for tg_chat_id in config['GENERAL']['TG_FORWARD_IDES'].split(' '):
        await client.send_poll(tg_chat_id.replace('https://t.me/', ''),
                               question=message.poll.question,
                               is_anonymous=message.poll.is_anonymous,
                               options=[option.text for option in message.poll.options],
                               allows_multiple_answers=message.poll.allows_multiple_answers,
                               correct_option_id=message.poll.correct_option_id,
                               explanation=message.poll.explanation)


async def media_group(client, message, m_group):
    media_list = []

    for media in m_group:
        if media.photo:
            media_list.append(types.InputMediaPhoto(media.photo.file_id, caption=media.caption or ""))
        elif media.video:
            media_list.append(types.InputMediaVideo(media.video.file_id, caption=media.caption or ""))

    for tg_chat_id in config['GENERAL']['TG_FORWARD_IDES'].split(' '):
        await client.send_media_group(chat_id=tg_chat_id.replace(r'https://t.me/', ''), media=media_list)
