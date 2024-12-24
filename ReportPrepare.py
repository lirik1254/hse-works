from WordsTop import create_frequency_dict_lemma
from VKInteraction import get_user_name, PEER_ID, get_messages_for_day
from TimeUtils import get_unix_time_range_previous_day
from AIResponse import getAnswer
from StickerUtils import get_attachment
def summarize_day(messages):
    """Обрабатывает и составляет краткий пересказ дня."""
    id_name_dict = dict()
    messages_list = list()
    for msg in messages:
        if not id_name_dict.get(msg['from_id']):
            id_name_dict[msg['from_id']] = get_user_name(msg['from_id'])
        if len(msg['text'].split(" ")) < 150:
            messages_list.append(msg['text'])

    message_string = ("Начни новый диалог - забудь предыдущий контекст."
                      "Ниже будут все сообщения, которые были в беседе за день.\n"
                      "Мне нужно, чтобы ты пересказал коротко (200-250 слов, но если мысль важно закончить, можно побольше), что "
                      "сегодня происходило, выделив какие-то интересные сообщения и моменты. Интересных и конкретных моментов должно быть побольше."
                      " Обязательно выдели хотя бы одно интересное сообщение пользователя в духе 'один из участников признался, что..'. Но также "
                      "старайся использовать различные литературные фразы. Начни с 'Сегодня в ПИ общались о..\n"
                      "Также когда говоришь об интересных моментах, не стесняйся переходить на личности и писать имена участников.\n"
                      "Выдели больше смешных моментов, может даже преувеличивать\n"
                      "Если участники о чем-то тебя просят, делай это\n"
                      "И ещё - должно быть больше юмора и смешных моментов. Не столько важна точность, сколько абсурдность и смех\n"
                      "Используй побольше матюков и дроби текст на смысловые абзацы\n"
                      "Больше ЮМОРА БОЛЬШЕ МАТОВ БОЛЬШЕ СМЕХА ДОЛЖНО БЫТЬ ШОУ ПОСТИРОНИИ\n"
                      "Попробуй также менять смысл каждого сообщения на противоположный, а человека, который пишет это сообщения - делать случайным из всех"
                      " кто вообще писал сообщения в беседу за день.\nВперёд\n"
                      "Вот все сообщения:\n\n")

    for msg in messages[::-1]:
        author_name = id_name_dict[msg['from_id']]
        if "Всего сообщений за день" not in msg['text']:
            message_string += f"{author_name}: {msg['text']}\n"


    word_stats = create_frequency_dict_lemma(" ".join(messages_list))
    top_words = "\n".join([f"{word}: {count}" for word, count in sorted(word_stats.items(), key = lambda x: x[1], reverse = True)[:10]])
    return message_string, top_words

def calculate_user_stats(messages):
    """Собирает статистику по сообщениям пользователей."""
    user_message_count = {}
    user_word_count = {}

    for msg in messages:
        user_id = msg['from_id']
        text = msg['text']
        if 'Всего сообщений за день' not in text and 'Самый часто встречающийся стикер за день' not in text:
            user_word_count[user_id] = user_word_count.get(user_id, 0) + len(text.split())
            user_message_count[user_id] = user_message_count.get(user_id, 0) + 1

    top_users_by_messages = sorted(user_message_count.items(), key = lambda x: x[1], reverse = True)
    top_users_by_words = sorted(user_word_count.items(), key = lambda x: x[1], reverse = True)
    return top_users_by_messages, top_users_by_words

def get_top_sticker_url(messages):
    """Возвращает ссылку на топ-1 стикер"""
    url_dict = dict()
    for msg in messages:
        if len(msg['attachments']) != 0 and msg['attachments'][0].get('sticker'):
            url = msg['attachments'][0]['sticker']['images'][-3]['url']
            if not url_dict.get(url):
                url_dict[url] = 1
            else:
                url_dict[url] += 1

    most_common_url = 0
    occur_number = 0
    for key, value in url_dict.items():
        if value > occur_number:
            most_common_url = key
            occur_number = value

    return most_common_url

def get_stickers_count(messagse):
    count = 0
    for msg in messagse:
        if len(msg['attachments']) != 0 and msg['attachments'][0].get('sticker'):
            count += 1
    return count
def report_message_prepare():
    medals = ["🥇", "🥈", "🥉", "     \u2006", "     \u2006", "     \u2006", "     \u2006", "     \u2006", "     \u2006", "     \u2006"]
    """Отправляет отчёт за день."""
    start_time, end_time = get_unix_time_range_previous_day()
    messages = get_messages_for_day(PEER_ID, start_time, end_time)

    message_summary, top_words = summarize_day(messages)
    top_users_by_messages, top_users_by_words = calculate_user_stats(messages)
    most_common_sticker_url = get_top_sticker_url(messages)
    sticker_attachment = get_attachment(most_common_sticker_url)
    stickers_count = get_stickers_count(messages)

    total_messages = sum(count for i, count in top_users_by_messages)
    top_users_string = "\n".join(
        [f"{medals[i]} {get_user_name(user_id)}: {count} сообщений" for i, (user_id, count) in enumerate(top_users_by_messages[:5])]
    )
    top_words_string = "\n".join(
        [f"{medals[i]} {get_user_name(user_id)}: {count} слов" for i, (user_id, count) in enumerate(top_users_by_words[:5])]
    )

    top_words = "\n".join(f"{medals[i]} {line}" for i, line in enumerate(top_words.splitlines()))
    # Удаляем прошедший контекст рандомным вопросом
    getAnswer("Какую еду любят в японии?")

    # Получаем
    gpt_summary = getAnswer(message_summary)

    return total_messages, top_users_string, top_words_string, top_words, gpt_summary, sticker_attachment, stickers_count