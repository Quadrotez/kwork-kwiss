from functions import *
from pyrogram import filters, types, Client
import vk_api
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

    msg = message.text

    for vk_chat_id in config['GENERAL']['VK_FORWARDS_IDES'].split(' '):
        vk_api_client.method("messages.send", {"user_id": vk_chat_id, "random_id": 0,
                                               "message": msg})

print('Начало работы')
app.run()
