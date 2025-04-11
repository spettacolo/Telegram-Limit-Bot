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
account = Client("account", api_id=api_id, api_hash=api_hash)

waiting_list = [] # dict list [{'id':eta,...}]

async def is_admin_filter(_, __, message: Message):
  user = message.from_user
  return user.id == owner

is_admin = filters.create(is_admin_filter)

async def approve(user_id: int | str):
  global account
  await account.start()
  await account.get_users(user_id)
  rules = await account.get_privacy(enums.PrivacyKey.NO_PAID_MESSAGES)
  users = []
  for rule in rules:
    if rule.type == enums.PrivacyRuleType.ALLOW_USERS:
      users.extend([user.id for user in rule.users for rule in rules])
      users.append(user_id)
      break
  await account.set_privacy(
    enums.PrivacyKey.NO_PAID_MESSAGES,
    rules = [
      InputPrivacyRuleAllowUsers(users),
      InputPrivacyRuleAllowContacts()
    ]
  )
  await account.stop()
  return

@bot.on_message(filters.private & filters.command(["start", "help"]))
async def start_handler(bot: Client, message: Message):
  await message.reply("Hey! Send /request {reason} to unlock the chat with @balestra.")


@bot.on_message(filters.private & filters.command(["r", "req", "request"]))
async def request_handler(bot: Client, message: Message):
  global waiting_list
  user = message.from_user
  user_dict = {
    "user": user,
    "eta": time.time()
  }
  waiting_list.append()

@bot.on_message(filters.private & is_admin & filters.command(["approve", "ok", "allow"]))
async def approve_handler(bot: Client, message: Message):
  if len(message.text.split()) > 1:
    command, user_id = message.text.split()
    try:
      #msg = await bot.get_messages(chat_id=int(user_id) if user_id.isdigit() else user_id, message_ids=0)
      #print(user_id)
      #msg = await msg.forward(chat_id=7314203962, disable_notification=True)
      await approve(user_id)
      await message.reply(f"Approved {user_id}")
      #await msg.delete()
    except Exception as e:
      print(f"Error while approving: {e}")

@bot.on_message(filters.private)
async def wait_for_response_handler(bot: Client, message: Message):
  pass

#async def main(bot: Client, account: Client):
#  await compose([bot, account])

if __name__ == "__main__":
  bot.run()
  #asyncio.run(main(bot, account))
