import json

import requests
import os
import time
from functions import *
from vk_api import VkUpload
from config import *
from pyrogram import Client, types

config = init.config()


async def upload_photo(client, api, message):
    path_temp_photo = os.path.join(temp_path, f'{time.time()}.jpg')
    await client.download_media(message.photo.file_id,
                                file_name=path_temp_photo)
    photo_info = VkUpload(api).photo_wall(photos=path_temp_photo)[0]
    os.remove(path_temp_photo)
    return f'photo{photo_info["owner_id"]}_{photo_info["id"]}'


async def photo(client, message, api):
    for vk_chat_id in config['GENERAL']['VK_FORWARD_IDES'].split(' '):
        api.wall.post(owner_id=f'-{vk_chat_id}', message=message.caption,
                      attachment=await upload_photo(client, api, message))


async def upload_video(client, api, message):
    path_temp_video = os.path.join(temp_path, f'{time.time()}.mp4')
    video_info = api.video.save(name=" ", description=" ", is_private=0,
                                wallpost=1, repeat=1)
    upload_url = video_info['upload_url']
    with open(await client.download_media(message.video.file_id,
                                          file_name=path_temp_video), 'rb') as video_file:
        requests.post(upload_url, files={'video_file': video_file})
    os.remove(path_temp_video)

    return f"video{video_info['owner_id']}_{video_info['video_id']}"


async def video(client, message, api):
    uploaded_video = await upload_video(client, api, message)
    for vk_chat_id in config['GENERAL']['VK_FORWARD_IDES'].split(' '):
        api.wall.post(owner_id=f'-{vk_chat_id}', from_group=1, message=message.caption,
                      attachments=uploaded_video)


async def poll(client: Client, message: types.Message, api):
    poll_info = api.polls.create(question=message.poll.question,
                                 add_answers=json.dumps([answer.text for answer in message.poll.options]),
                                 is_anonymous=int(message.poll.is_anonymous),
                                 is_multiple=int(message.poll.allows_multiple_answers))

    for vk_chat_id in config['GENERAL']['VK_FORWARD_IDES'].split(' '):
        api.wall.post(
            owner_id=f'-{vk_chat_id}',  # ID группы с минусом
            from_group=1,
            attachments=f'poll{poll_info["owner_id"]}_{poll_info["id"]}'  # Прикрепляем созданный опрос
        )


async def media_group(client, message, api, m_group):
    attachments = []
    for media in m_group:
        if media.video:
            attachments.append(await upload_video(client, api, media))
        elif media.photo:
            attachments.append(await upload_photo(client, api, media))

    for vk_chat_id in config['GENERAL']['VK_FORWARD_IDES'].split(' '):
        api.wall.post(owner_id=f'-{vk_chat_id}', from_group=1, message=message.caption,
                      attachments=','.join(attachments))
