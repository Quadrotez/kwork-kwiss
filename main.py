import os
import time
import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from functions import *
from pyrogram import filters, types, Client
from config import *
import ok_api

config = init.config()

app = init.client()

vk_api_client = vk_api.VkApi(token=config['GENERAL']['VK_TOKEN'])

with app:
    channel_check_id = app.get_chat(config['GENERAL']['CHANNEL_CHECK']).id


@app.on_message()
async def main_handler(client: Client, message: types.Message):
    if message.chat.id != channel_check_id:
        return

    api = vk_api_client.get_api()

    if message.photo and message.caption:
        path_temp_photo = os.path.join(temp_path, f'{time.time()}.jpg')
        await client.download_media(message.photo.file_id,
                                    file_name=path_temp_photo)
        photo = VkUpload(api).photo_wall(photos=path_temp_photo)[0]
        for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
            api.wall.post(owner_id=f'-{vk_chat_id}', message=message.caption,
                          attachment=f'photo{photo["owner_id"]}_{photo["id"]}')

        os.remove(path_temp_photo)

    elif message.video and message.caption:
        print('dsad')
        path_temp_video = os.path.join(temp_path, f'{time.time()}.mp4')

        for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
            video_info = api.video.save(
                name="Название видео",
                description="Описание видео",
                group_id=vk_chat_id,  # ID сообщества
                is_private=0,  # 0 - публичное, 1 - приватное
                wallpost=0,  # 0 - не публиковать сразу, 1 - публиковать сразу
                repeat=1,  # 1 - видео будет повторяться
            )

            # Загрузка файла на полученный URL
            upload_url = video_info['upload_url']
            with open(await client.download_media(message.photo.file_id,
                                                  file_name=path_temp_video), 'rb') as video_file:
                requests.post(upload_url, files={'video_file': video_file})
            api.wall.post(owner_id=f'-{vk_chat_id}', from_group=1, message=message.caption,
                          attachments=f"video{video_info['owner_id']}_{video_info['video_id']}")

        os.remove(path_temp_video)

    # for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
    #     api.wall.post(owner_id=f'-{vk_chat_id}', from_group=1, message=msg, signed=0, attachments=[], v='5.131')
    #
    # for tg_chat_id in config['GENERAL']['TG_PASSWORD_IDES'].split(' '):
    #     await client.send_message(tg_chat_id.replace('https://t.me/', ''), msg)


print('Начало работы')
app.run()
