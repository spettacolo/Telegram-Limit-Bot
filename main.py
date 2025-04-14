from pyrogram import Client, filters, compose, enums, types
from pyrogram.types import Message, User, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv
import asyncio, time, os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

owner = os.getenv("OWNER")

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
bot_data = None

async def is_admin_filter(_, __, message: Message):
  user = message.from_user
  return user.id == owner

is_admin = filters.create(is_admin_filter)

@bot.on_message(filters.private & filters.command(["start", "help"]))
async def start_handler(bot: Client, message: Message):
  global bot_data
  bot_data = await bot.get_me()
  await message.reply("Hey!")

@bot.on_message(filters.private)
async def new_message_handler(bot: Client, message: Message):
  global bot_data
  reply_markup = InlineKeyboardMarkup(
    [
      [InlineKeyboardButton("View Profile", user_id=message.from_user.id)], #pyrogram.errors.exceptions.bad_request_400.ButtonUserPrivacyRestricted: Telegram says: [400 BUTTON_USER_PRIVACY_RESTRICTED] - The privacy settings of the user specified in a keyboard button do not allow creating such button (caused by "messages.SendMessage")
      #[InlineKeyboardButton("Send Message", callback_data=f"send_message_{message.from_user.id}")],
      [InlineKeyboardButton("Reply", url=f"t.me/{bot_data.username}?start={message.from_user.id},{message.id}")],
    ]
  )

  await message.copy(chat_id=owner, reply_markup=reply_markup)
  await message.reply("Message sent to owner.")

if __name__ == "__main__":
  bot.run()
