import requests
import os
import time
from functions import *
from vk_api import VkUpload
from config import *

config = init.config()


async def upload_photo(client, api, message):
    path_temp_photo = os.path.join(temp_path, f'{time.time()}.jpg')
    await client.download_media(message.photo.file_id,
                                file_name=path_temp_photo)
    photo_info = VkUpload(api).photo_wall(photos=path_temp_photo)[0]
    os.remove(path_temp_photo)
    return f'photo{photo_info["owner_id"]}_{photo_info["id"]}'


async def photo(client, api, message):
    for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
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


async def video(client, api, message):
    uploaded_video = await upload_video(client, api, message)
    for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
        api.wall.post(owner_id=f'-{vk_chat_id}', from_group=1, message=message.caption,
                      attachments=uploaded_video)



async def media_group(client, api, message, m_group):
    attachments = []
    for media in m_group:
        if type(media.video) is not None:
            attachments.append(upload_video(client, api, message))
        if type(media.photo) is not None:
            attachments.append(upload_photo(api))

    for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
        api.wall.post(owner_id=f'-{vk_chat_id}', from_group=1, message=message.caption,
                      attachments=','.join(attachments))
