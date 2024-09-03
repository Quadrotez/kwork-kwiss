from functions import *
from pyrogram import filters, types, Client


config = init.config()

app = init.client()


@app.on_message()
async def main_handler(client: Client, message: types.Message):
    if message.chat.id != (await app.get_chat(config['GENERAL']['CHANNEL_CHECK'])).id:
        return

    print('da')


app.run()