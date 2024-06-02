from pyrogram import Client
from dotenv import load_dotenv
import os
import csv

load_dotenv()

CONFIG = {
    "telegram_api_id": int(os.getenv("TG_API_ID")),
    "telegram_hash": os.getenv("TG_API_HASH"),
}


app = Client("my_account",CONFIG["telegram_api_id"],CONFIG["telegram_hash"])

chat_id = "tikvahethiopia"

async def main():
    async with app:
        async for message in app.get_chat_history(chat_id):
            row_data = message.text
            print(row_data)

app.run(main())

