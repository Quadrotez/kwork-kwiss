import traceback
import vk_api
import asyncio
import re

from pyrogram import types, Client, errors
from functions import *

config = init.config()

app = init.client()

vk_api_session = vk_api.VkApi(token=config['GENERAL']['VK_TOKEN'])
vk_api_client = vk_api_session.get_api()

with app:
    try:
        channel_check_id = app.get_chat(config['GENERAL']['CHANNEL_CHECK']).id
    except errors.exceptions.bad_request_400.PeerIdInvalid:
        channel_check_id = config['GENERAL']['CHANNEL_CHECK']



@app.on_message()
async def main_handler(client: Client, message: types.Message):
    # Проверка принадлежности сообщения к чату-источнику, присутствия в вайт-листе, отсутствия в блек-листе
    if (message.chat.id != channel_check_id and
        re.search(config['GENERAL']['WHITE_LIST'],
                  message.text if message.text else message.caption if message.caption else '') and
        not re.search(config['GENERAL']['BLACK_LIST'],
                      message.text if message.text else message.caption if message.caption else '')):
        return

    # Задержка
    await asyncio.sleep(int(config['GENERAL']['DELAY']))

    # Если после задержки сообщение было удалено, остановить выполнение функции
    if not await client.get_messages(message.chat.id, message.id):
        return

    # Обработчик Media Group
    if message.media_group_id and message.caption:
        try:
            media_group = await client.get_media_group(message.chat.id, message.id)
            await send.vk.media_group(client, message, vk_api_client, media_group)
            await send.tg.media_group(client, vk_api_client, media_group)
        except Exception as e:
            await client.send_message(config['GENERAL']['ADMIN_CHAT'], f'Произошла ошибка: {e}')

    # Обработчик Photo
    elif message.photo and message.caption:
        try:
            await send.vk.photo(client, message, vk_api_client)
            await send.tg.photo(client, message)
        except:
            await client.send_message(config['GENERAL']['ADMIN_CHAT'],
                                      f'Произошла ошибка: {traceback.format_exc()}')

    # Обработчик Video
    elif message.video and message.caption:
        try:
            await send.vk.video(client, message, vk_api_client)
            await send.tg.video(client, message)
        except Exception as e:
            await client.send_message(config['GENERAL']['ADMIN_CHAT'], f'Произошла ошибка: {e}')

    # Обработчик Poll
    elif message.poll:
        try:
            await send.vk.poll(client, message, vk_api_client)
            await send.tg.poll(client, message)
        except Exception as e:
            await client.send_message(config['GENERAL']['ADMIN_CHAT'], f'Произошла ошибка: {e}')


print('Начало работы')
app.run()
