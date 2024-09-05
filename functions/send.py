import os
import time
import requests
from config import *
from pyrogram import Client, types
from vk_api import VkUpload, VkApi
from functions import *

config = init.config()


async def photo(client: Client, api, message: types.Message):
    path_temp_photo = os.path.join(temp_path, f'{time.time()}.jpg')
    await client.download_media(message.photo.file_id,
                                file_name=path_temp_photo)
    photo_info = VkUpload(api).photo_wall(photos=path_temp_photo)[0]
    for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
        api.wall.post(owner_id=f'-{vk_chat_id}', message=message.caption,
                      attachment=f'photo{photo_info["owner_id"]}_{photo_info["id"]}')

    for tg_chat_id in config['GENERAL']['TG_PASSWORD_IDES'].split(' '):
        await client.send_photo(tg_chat_id.replace('https://t.me/', ''), photo=path_temp_photo,
                                caption=message.caption)

    os.remove(path_temp_photo)


async def video(client: Client, api, message: types.Message):
    path_temp_video = os.path.join(temp_path, f'{time.time()}.mp4')

    for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
        video_info = api.video.save(name=" ", description=" ", group_id=vk_chat_id, is_private=0,
                                    wallpost=1, repeat=1)

        upload_url = video_info['upload_url']
        with open(await client.download_media(message.video.file_id,
                                              file_name=path_temp_video), 'rb') as video_file:
            requests.post(upload_url, files={'video_file': video_file})
        api.wall.post(owner_id=f'-{vk_chat_id}', from_group=1, message=message.caption,
                      attachments=f"video{video_info['owner_id']}_{video_info['video_id']}")

    for tg_chat_id in config['GENERAL']['TG_PASSWORD_IDES'].split(' '):
        await client.send_video(tg_chat_id.replace('https://t.me/', ''), video=path_temp_video,
                                caption=message.caption)

    os.remove(path_temp_video)


async def media_group(client: Client, api, message: types.Message, m_group):
    for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
        attachments = []
        for media in m_group:
            if type(media.video) is not None:
                print(media.video, type(media.video))
                path_temp_video = os.path.join(temp_path, f'{time.time()}.mp4')
                video_info = api.video.save(name=" ", description=" ", is_private=0,
                                            wallpost=1, repeat=1)

                upload_url = video_info['upload_url']
                with open(await client.download_media(message.video.file_id,
                                                      file_name=path_temp_video), 'rb') as video_file:
                    requests.post(upload_url, files={'video_file': video_file})

                attachments.append(f"video{video_info['owner_id']}_{video_info['video_id']}")
            if type(media.photo) is not None:
                print(media.photo)
                path_temp_photo = os.path.join(temp_path, f'{time.time()}.jpg')
                await client.download_media(message.photo.file_id,
                                            file_name=path_temp_photo)
                photo_info = VkUpload(api).photo_wall(photos=path_temp_photo)[0]
                attachments.append(f'photo{photo_info["owner_id"]}_{photo_info["id"]}')

        api.wall.post(owner_id=f'-{vk_chat_id}', from_group=1, message=message.caption,
                      attachments=','.join(attachments))

    for tg_chat_id in config['GENERAL']['TG_PASSWORD_IDES'].split(' '):
        media_list = []

        for media in m_group:
            if media.photo:
                media_list.append(types.InputMediaPhoto(media.photo.file_id, caption=media.caption))
            elif media.video:
                media_list.append(types.InputMediaVideo(media.video.file_id, caption=media.caption))
        await client.send_media_group(tg_chat_id.replace('https://t.me/', ''), media=media_list)
