from telethon import TelegramClient, sync, events
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH
from datetime import datetime
from time import sleep
import getpass
import json
import vk_api
print("Аутентификация пользователя в ВКонтакте.")
username = input("Введите номер телефона или email: ")
password = getpass.getpass("Введите пароль: ")

vk_session = vk_api.VkApi(username, password)
vk_session.auth()

vk = vk_session.get_api()

owner_id = -1 * int(input("Введите id сообщества, где вы имеете доступ к сообщениям: "))
session_name = "DeploySession"
client = TelegramClient(session_name, TELEGRAM_API_ID, TELEGRAM_API_HASH)

print("Далее введите имя канала или id, если каналов с таким названием несклько.")
sepcific_channel_id = input("Введите имя канала: ")
with open("new_messages.json", "w") as f:
    f.write("{}")


@client.on(events.NewMessage(chats=(sepcific_channel_id)))
async def handle_channel_messages(event):
    msg_to_dict = event.message.to_dict()
    message_text = msg_to_dict["message"]
    message_date = msg_to_dict["date"]
    message_id = msg_to_dict["id"]

    with open("new_messages.json", "r", encoding="utf-8") as f:
        json_str = f.read().strip()
    now_json = json.loads(json_str)
    now_json[message_id] = {"text" : message_text, "date" : message_date.strftime("%d-%m-%Y %H:%M")}
    # print(now_json)
    to_write = json.dumps(now_json, ensure_ascii=False)
    # print(to_write)
    with open("new_messages.json", "w", encoding="utf-8") as f:
        f.write(to_write)
    await vk.wall.post(owner_id=owner_id, message=message_text)

def start(client):
    client.start()
    client.run_until_disconnected()