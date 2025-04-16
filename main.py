from pyrogram import Client, filters, compose, enums, types
from pyrogram.types import Message, User, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import BadRequest
from dotenv import load_dotenv
import asyncio, time, os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

owner = os.getenv("OWNER")

first_time_start_command = True

waiting_list = [] # --> [{"admin_id": 1234, "user_id": 1234, "message_id": 1234}, ...]

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
bot_data = None

async def is_admin_filter(_, __, message: Message):
    user = message.from_user
    return user.id == owner

is_admin = filters.create(is_admin_filter)

async def manager():
    pass

@bot.on_callback_query(filters.regex(r"view_profile_(\d+)"))
async def view_profile_handler(bot: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])
    user = await bot.get_users(user_id)

    profile_details = f"User ID: {user.id}\nFirst Name: {user.first_name}" #Username: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}"
    if user.last_name:
        profile_details += f"\nLast Name: {user.last_name}"
        if user.username:
        profile_details += f"\nUsername: @{user.username}"
    if user.raw.photo:
        photo_binary = await bot.download_media(user.photo.big_file_id, in_memory=True)
        await callback_query.message.reply_photo(photo=photo_binary, caption=profile_details)
    else:
        await callback_query.message.reply(text=profile_details)

    await callback_query.answer()

@bot.on_callback_query(filters.regex(r"reply_(\d+)_(\d+)"))
async def reply_to_user(bot: Client, callback_query: CallbackQuery):
    callback_data, user_id, message_id = callback_query.data.split("_")
    user_id = int(user_id)
    message_id = int(message_id)

    await callback_query.message.reply(text="Send the message you want to forward as a reply:")

    await callback_query.answer()

@bot.on_message(filters.private & filters.command(["start", "help"]))
async def start_handler(bot: Client, message: Message):
    global bot_data, owner, first_time_start_command
    # print(message)
    if first_time_start_command:
        bot_data = await bot.get_me()
    if message.from_user.id == owner:
        print(1)
    else:
        await message.reply("Hey! Send me a message to forward it to Falzy")

@bot.on_message(filters.private)
async def new_message_handler(bot: Client, message: Message):
    global bot_data
    reply_markup = InlineKeyboardMarkup(
        [
        [InlineKeyboardButton("View Profile", callback_data=f"view_profile_{message.from_user.id}")],
        #[InlineKeyboardButton("Send Message", callback_data=f"send_message_{message.from_user.id}")],
        [InlineKeyboardButton("Reply", callback_data=f"reply_{message.from_user.id}_{message.id}")],
        ]
    )

    await message.copy(chat_id=owner, reply_markup=reply_markup)
    await message.reply("Message sent to owner.")

if __name__ == "__main__":
  bot.run()
