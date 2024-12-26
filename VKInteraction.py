import os
import time
import vk_api

from Utils.ReturnGraphicUtils import return_graphic

# Чтобы получить токен VK, зайди https://vkhost.github.io/, выбери VK Admin, далее следуй инструкции на сайте
# После зайди в системные переменные, добавь новую переменную с названием VK_TOKEN и значением - твоим токеном, перезагрузи среду разработки.
token = os.getenv("VK_TOKEN")

PEER_ID = 2000000000 + 234  # ID Беседы ПИ. НЕ ОТПРАВЛЯЙТЕ НИЧЕГО ТУДА, МЕНЯЙТЕ В SEND_REPORT НА ДРУГОЙ ID
#PEER_ID = 2000000000 + 90
# Инициализация сессии
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()



# Функция для получения сообщений за сутки
def get_messages_for_day(peer_id, start_time, end_time):
    messages = []
    offset = 0
    count = 200  # Максимум сообщений за один запрос

    while True:
        response = vk.messages.getHistory(
            peer_id = peer_id,
            count = count,
            offset = offset
        )

        # Добавляем полученные сообщения в список
        messages.extend(response['items'])

        # Прекращаем запросы, если первое сообщение в ответе старше нужной даты
        if response['items'] and response['items'][-1]['date'] < start_time:
            break

        time.sleep(1)
        offset += count

    # Фильтрация сообщений по времени
    filtered_messages = [msg for msg in messages if start_time <= msg['date'] < end_time]
    return filtered_messages


# Функция для получения имени и фамилии по ID
def get_user_name(user_id):
    if user_id < 0:  # Если ID отрицательный, это группа
        return f"Группа {abs(user_id)}"
    user_info = vk.users.get(user_ids = user_id)[0]
    return f"{user_info['first_name']} {user_info['last_name']}"


def send_report(peer_id):
    from ReportPrepare import report_message_prepare
    total_messages, top_users_string, top_words_string, top_words, gpt_summary, sticker_attachment, stickers_count, reactions_count, reactions_top, username_top_five_for_reactions_count_string = report_message_prepare()
    msgs_by_time_attachment = return_graphic(vk, "Photo/messages_by_time.png")
    sentiment_attachment = return_graphic(vk, "Photo/sentiment_pie_chart.png")

    report = (
        f"Всего сообщений за день: {total_messages}\n"
        f"Из них стикеров: {stickers_count}\n\n"
        f"Всего реакций за день: {reactions_count}\n\n"
        f"🏆 Топ 5 по количеству сообщений:\n{top_users_string}\n\n"
        f"🏆 Топ 5 по количеству слов:\n{top_words_string}\n\n"
        f"🏆 Топ 5 по количеству полученных реакций:\n{username_top_five_for_reactions_count_string}\n\n"
        f"🏆 Топ 5 реакций за день:\n{reactions_top}\n\n"
        f"🏆 Топ 10 слов за день:\n{top_words}\n\n"
        f"🤠 Краткий пересказ, о чем говорили за день:\n\n{gpt_summary}\n\n"
    )
    # Чтобы отправлять не в ту же беседу, откуда парсились сообщения - замени peer_id на нужный параметр
    vk.messages.send(peer_id=peer_id, message=report, random_id=int(time.time()))
    time.sleep(1)

    vk.messages.send(peer_id=peer_id, message="🏆 Самый часто встречающийся за день стикер",
                     attachment=sticker_attachment, random_id=int(time.time()))
    time.sleep(1)

    vk.messages.send(peer_id=peer_id, message="",
                     attachment=msgs_by_time_attachment, random_id=int(time.time()))
    time.sleep(1)

    vk.messages.send(peer_id=peer_id, message="",
                     attachment=sentiment_attachment, random_id=int(time.time()))
    time.sleep(1)
