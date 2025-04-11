from pyrogram import Client, filters, compose, enums, types
from pyrogram.types import Message, User, InputPrivacyRuleAllowUsers, InputPrivacyRuleAllowContacts
from dotenv import load_dotenv
import asyncio, time, os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

owner = os.getenv("OWNER")

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

async def is_admin_filter(_, __, message: Message):
  user = message.from_user
  return user.id == owner

is_admin = filters.create(is_admin_filter)

@bot.on_message(filters.private & filters.command(["start", "help"]))
async def start_handler(bot: Client, message: Message):
  await message.reply("Hey!")

@bot.on_message(filters.private)
async def wait_for_response_handler(bot: Client, message: Message):
  pass

if __name__ == "__main__":
  bot.run()
