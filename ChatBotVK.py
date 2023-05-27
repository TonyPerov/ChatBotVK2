import datetime
import vk_api
import sqlite3
from vk_api.longpoll import VkLongPoll, VkEventType


# vk1.a.4pi3i8tho9KfuHXC3to7CGpG452539M8NjPAVj9kNktwJ8jujgW5QNvPqxPL38ROJAzZbfL10uabzuKhRXt4F9dA2PpCpQalNnnTpyn9B0lQUpg5qtdiFFKjPnZJvAD2ZB3o2MI0NDfsYUX_1_eUBNdkOQa6dKsYHdvP74Iz1pu6ePozMtW5Bw2FFqMwzG7d_Jl7mjRoOAjrz5MDrKP8SQ

# <Имя бота> сохрани фразу <фраза>
# <Имя бота> напиши фразу

class Vk_Bot:
    def __init__(self, bot_name, api_token):
        self.session = vk_api.VkApi(token=api_token)
        self.longpoll = VkLongPoll(self.session)
        self.vk = self.session.get_api()
        self.bot_name = bot_name
        self.conn = sqlite3.connect(self.bot_name + ".db")

    def send_message(self, message, id):
        self.vk.messages.send(user_id=id, message=message, random_id=datetime.datetime.now().microsecond)

    def start(self):
        init_db = open("init_db.sql")
        raw_init = init_db.readlines()
        init = ""
        for line in raw_init:
            init += line.replace("\n", " ")
        self.conn.execute(init)
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command_words = event.text.split(" ")
                if command_words[0] == self.bot_name:
                    if len(command_words) > 3 and command_words[1] == "сохрани" and command_words[2] == "фразу":
                        phrase = event.text[15 + len(self.bot_name):]
                        self.conn.execute(
                            f'INSERT OR REPLACE INTO user_info(vk_id, sentence) VALUES ({event.user_id}, "{phrase}")')
                        self.conn.commit()
                        self.send_message(f'Фраза "{phrase}" успешно сохранена!', event.user_id)
                    if len(command_words) > 2 and command_words[1] == "напиши" and command_words[2] == "фразу":
                        answer = self.conn.execute(
                            f"SELECT sentence FROM user_info WHERE vk_id = {event.user_id}").fetchall()
                        if len(answer) > 0:
                            answer = answer[0][0]
                            self.send_message(f'Да, конечно! Вот ваша фраза: "{answer}"', event.user_id)
                        else:
                            self.send_message('Ошибка: вы не сохраняли никакую фразу', event.user_id)


bot = Vk_Bot("KvantBot",
             "vk1.a.4pi3i8tho9KfuHXC3to7CGpG452539M8NjPAVj9kNktwJ8jujgW5QNvPqxPL38ROJAzZbfL10uabzuKhRXt4F9dA2PpCpQalNnnTpyn9B0lQUpg5qtdiFFKjPnZJvAD2ZB3o2MI0NDfsYUX_1_eUBNdkOQa6dKsYHdvP74Iz1pu6ePozMtW5Bw2FFqMwzG7d_Jl7mjRoOAjrz5MDrKP8SQ")
bot.start()

# GitHub
#:(
