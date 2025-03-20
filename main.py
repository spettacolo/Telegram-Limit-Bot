from pyrogram import Client, filters, enums, compose
from pyrogram.types import Message, User, InputPrivacyRuleAllowUsers, InputPrivacyRuleAllowContacts
from dotenv import load_dotenv
import asyncio, time, os

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
account = Client("account", api_id=api_id, api_hash=api_hash)

waiting_list = [] # dict list [{'id':eta,...}]

async def is_admin_filter(user: User):
  return user.id == 7314203962

is_admin = filters.create(is_admin_filter)

async def approve(user_id: int):
  global account
  rules = await account.get_privacy(enums.PrivacyKey.NO_PAID_MESSAGES)
  users = []
  for rule in rules:
    if rule.type == enums.PrivacyRuleType.ALLOW:
      users.extend([user.id for user in rules.users])
      users.append(user_id)
      break
  await account.set_privacy(
    enums.PrivacyKey.NO_PAYD_MESSAGES,
    rules = [
      InputPrivacyRuleAllowUsers(users),
      InputPrivacyRuleAllowContacts()
    ]
  )

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
      await bot.get_users(user_id)
      await approve()
    except Exception as e:
      print(f"Error while approving: {e}")

@bot.on_message(filters.private)
async def wait_for_response_handler(bot: Client, message: Message):
  pass

async def main(bot: Client, account: Client):
  await compose([bot, account])

if __name__ == "__main__":
  asyncio.run(main(bot, account))
