import time

import requests
import vk_api
from pyrogram import types, Client
from vk_api import VkUpload

from config import *
from functions import *

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

    if message.media_group_id:
        print('Media group')
        if message.media_group_id:
            await send.media_group(client, api, message, await client.get_media_group(message.chat.id, message.id))

    elif message.photo and message.caption:
        print('Photo')
        await send.photo(client, api, message)

    elif message.video and message.caption:
        print('Video')
        await send.video(client, api, message)

print('Начало работы')
app.run()
