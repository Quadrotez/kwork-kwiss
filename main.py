import vk_api
from pyrogram import types, Client

from functions import *

config = init.config()

app = init.client()

vk_api_session = vk_api.VkApi(token=config['GENERAL']['VK_TOKEN'])
vk_api_client = vk_api_session.get_api()

with app:
    channel_check_id = app.get_chat(config['GENERAL']['CHANNEL_CHECK']).id


@app.on_message()
async def main_handler(client: Client, message: types.Message):
    if message.chat.id != channel_check_id:
        return

    if message.media_group_id and message.caption:
        print('Media group')
        media_group = await client.get_media_group(message.chat.id, message.id)
        await send.vk.media_group(client, message, vk_api_client, media_group)
        await send.tg.media_group(client, vk_api_client, media_group)

    elif message.photo and message.caption:
        print('Photo')
        await send.vk.photo(client, message, vk_api_client)
        await send.tg.photo(client, message)

    elif message.video and message.caption:
        print('Video')
        await send.vk.video(client, message, vk_api_client)
        await send.tg.video(client, message)

    elif message.poll:
        print('Poll')
        await send.vk.poll(client, message, vk_api_client)

print('Начало работы')
app.run()
