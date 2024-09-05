import time
import asyncio
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

    if message.media_group_id and message.caption:
        print('Media group')

        await send.vk.media_group(client, api, message, message,
                                  await client.get_media_group(message.chat.id, message.id))

    elif message.photo and message.caption:
        print('Photo')
        await send.vk.photo(client, api, message)
        await send.tg.photo(client, message)

    elif message.video and message.caption:
        print('Video')
        await send.vk.video(client, api, message)
        await send.tg.video(client, message)

print('Начало работы')
app.run()
