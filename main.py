from pyrogram import Client, filters
from pyrogram.types import Message, User
from dotenv import load_dotenv
import asyncio, time, os

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
account = Client("account", api_id=api_id, api_hash=api_hash)

waiting_list = [] # dict list [{'id':eta,...}]

@bot.on_message(filters.private & filters.command(["start", "help"])
async def start(bot: Client, message: Message):
  await message.reply("Hey! Send /request {reason} to unlock the chat with @balestra.")


@bot.on_message(filters.private & filters.command(["r", "req", "request"])
async def start(bot: Client, message: Message):
  global waiting_list
  user = message.from_user
  user_dict = {
    "user": user,
    "eta": time.time()
  }
  waiting_list.append()

@bot.on_message(filters.private)
async def wait_for_response(bot: Client, message: Message):
  pass

if __name__ == "__main__":
  bot.run()
