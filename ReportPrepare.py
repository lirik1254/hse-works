from WordsTop import create_frequency_dict_lemma
from VKInteraction import get_user_name, PEER_ID, get_messages_for_day
from TimeUtils import get_unix_time_range_previous_day
from AIResponse import getAnswer

def summarize_day(messages):
    """Обрабатывает и составляет краткий пересказ дня."""
    id_name_dict = dict()
    messages_list = list()
    for msg in messages:
        id_name_dict[msg['from_id']] = get_user_name(msg['from_id'])
        if len(msg['text'].split(" ")) < 150:
            messages_list.append(msg['text'])

    message_string = ("Начни новый диалог - забудь предыдущий контекст."
                      "Ниже будут все сообщения, которые были в беседе за день.\n"
                      "Мне нужно, чтобы ты пересказал коротко (200-250 слов, но если мысль важно закончить, можно побольше), что "
                      "сегодня происходило, выделив какие-то интересные сообщения и моменты. Интересных и конкретных моментов должно быть побольше."
                      " Обязательно выдели хотя бы одно интересное сообщение пользователя в духе 'один из участников признался, что..' Начни с 'Сегодня в ПИ общались о..\n"
                      "Также когда говоришь об интересных моментах, не стесняйся переходить на личности и писать имена участников.\n"
                      "Выдели больше смешных моментов, может даже преувеличивать\n"
                      "Если участники о чем-то тебя просят, делай это\n"
                      "И ещё - должно быть больше юмора и смешных моментов. Не столько важна точность, сколько абсурдность и смех\n"
                      "Используй побольше матюков и дроби текст на смысловые абзацы\n"
                      "Больше ЮМОРА БОЛЬШЕ МАТОВ БОЛЬШЕ СМЕХА ДОЛЖНО БЫТЬ ШОУ ПОСТИРОНИИ"
                      "Вот все сообщения:\n\n")

    for msg in messages[::-1]:
        author_name = id_name_dict[msg['from_id']]
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
        user_message_count[user_id] = user_message_count.get(user_id, 0) + 1
        user_word_count[user_id] = user_word_count.get(user_id, 0) + len(text.split())

    top_users_by_messages = sorted(user_message_count.items(), key = lambda x: x[1], reverse = True)
    top_users_by_words = sorted(user_word_count.items(), key = lambda x: x[1], reverse = True)
    return top_users_by_messages, top_users_by_words

def report_message_prepare():
    """Отправляет отчёт за день."""
    start_time, end_time = get_unix_time_range_previous_day()
    messages = get_messages_for_day(PEER_ID, start_time, end_time)

    message_summary, top_words = summarize_day(messages)
    top_users_by_messages, top_users_by_words = calculate_user_stats(messages)

    total_messages = sum(count for i, count in top_users_by_messages)
    top_users_string = "\n".join(
        [f"{i + 1}) {get_user_name(user_id)}: {count} сообщений" for i, (user_id, count) in enumerate(top_users_by_messages[:5])]
    )
    top_words_string = "\n".join(
        [f"{i + 1}) {get_user_name(user_id)}: {count} слов" for i, (user_id, count) in enumerate(top_users_by_words[:5])]
    )

    # Удаляем прошедший контекст рандомным вопросом
    getAnswer("Какую еду любят в японии?")

    # Получаем
    gpt_summary = getAnswer(message_summary)

    return total_messages, top_users_string, top_words_string, top_words, gpt_summary