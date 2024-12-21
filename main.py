import vk_api
from datetime import datetime, timedelta
import time
import pytz
from model import getAnswer
from words_top import create_frequency_dict_lemma

# Ваш токен доступа
token = 'vk1.a.BsUTzoBhATd1LUr-6wokayDeTOfppOnTWa5cxR6VPsJ95C7ln323rw_IXgGql_LNLUVvJ19jXA1Z6iuU0hCXHkqhWjo_kGZK_mIXOVyrPmqorAhFP60EcXwmXKtCMvEs9L_1fYL-uYSy6T8XBQ7_mJjxXYrCt4HcXzX-lNvLRUnJ8WKQHOyiXxdH_xj1aTQvohZVgtr-iDlW6-jIc6BOHw'

# ID беседы
peer_id = 2000000000 + 234  # Пример для чата с ID 234

# Инициализация сессии
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

matu = ("пизда, хуй, пизд, выебок, выебон, выблядок, блядун, бляхомуха, наёбка, наебка, наебнуть, "
        "впиздиться, впиздить, хуярить, хуя, ебанешься, ебан, ебалово, жидоёб, ёбля, ебля, ебнул, заебись, "
        "заебал, объебался, объебался, блять, бля, объёбус, объебусь, пиздеть, пиздить, уебался, уеб, хуйня, шароёбиться, "
        "шароебиться, шароебится, хуярить, пизда, хуй, бля, пизд, выебок,, выебон, выблядок, блядун, "
        "бляхомуха, наёбка, наебка, наебнуть, впиздиться, впиздить, хуярить, хуя, ебанешься, ебан, ебалово"
        ", жидоёб, ебля, ёбля, ебнул, заебись, заебал, объебался, блять, бля, объёбус, объебусь, пиздеть, пиздить, "
        "уебался, уеб, хуйня, шароёбиться, шароебиться, шароебится, хуярить, пизда, пиздит, пиздить, напиздел, напизжу, "
        "наебу, пизде, пизду, пизд, ебнула, ёбнула, ебнуло, ёбнуло, оттрахал, трахал, трахали, трахала, трахало, затрахали, затрахоло, оттрахали,"
        "оттрахало, пиздам, пизды, пизде, пиздой, пиздущей, ебал, ебали, ебало, ебалом, ебаный, ебаная, ебаные, ебучки, ебучка, ебучко, ебанько, ебаньки, хуи, "
        "хуями, хуях, хуи, сука, суки, сукам, суками, суках, пизда, пизды, пизде, пиздой, пизду, хуярю, хуярит, хуярят, хуярим, хуячат, хуячим, шароебимся, шароебитесь,"
        "ебалова, жидоёбы, жидоёбка, жидотварь, наебки, наебок, наебу, наебал, наебут, наебке, наебках, ебаны, ебанаты, ебанат, ебанушка, ебанатами, ебаната, "
        "ебанатах, уебок, уебки, уебков, уёбков, уёбкам, уебками, уебались, уебках, уёбках, блядунья, шлюха, шлюхи, шлюхам, шлюхами, шлюху, шлюхах, педик, пидорасы,"
        "пидорас, пидораса, пидорасу, пидорасами, пидорасов, пидорасах, гандон, гандона, гандонам, гандонами, гандонах, нахуй, похуй, пизды, похуям, ахуительный,"
        "ахуительные, ахуительная, хуи, ахуительнейшие, ахуительнейщая, ахуевшая, ахуевший, ахуел, ахуительный, ахуй, ебать, пиздец, ебу, спиздить, пиздеец, бляяяяя, бляя,"
        "бляяя, бляяяя, бляяяяя, бляяяяяя, бляяяяяя, бляяяяяяя, бляяяяяяяяяяяяяяяяяя, бляяяяяяяяяя, бляяяяяяя, бляяяяяяяяяяя")
matu_list = list(matu.split(", "))


def findMat(message):
    a = message.split(" ")
    for i in range(len(a)):
        a[i] = a[i].replace(",", "")
        a[i] = a[i].replace(".", "")
        a[i] = a[i].replace(":", "")
        a[i] = a[i].replace(")", "")
        a[i] = a[i].replace("(", "")
        a[i] = a[i].replace("!", "")
        a[i] = a[i].replace("+", "")
        a[i] = a[i].replace("$", "")
        a[i] = a[i].replace("*", "")
    for i in a:
        if i != "" and i in matu_list:
            return True
    return False


# Функция для получения UNIX-времени начала и конца суток
def get_unix_time_range():
    # Текущая дата и время с использованием pytz для Yekaterinburg
    tz = pytz.timezone('Asia/Yekaterinburg')
    now = datetime.now(tz)

    # Время начала вчерашнего дня (00:00)
    previous_day = now - timedelta(days=1)

    # Начало и конец предыдущего дня
    start_of_day = tz.localize(datetime(previous_day.year, previous_day.month, previous_day.day, 0, 0, 0))
    end_of_day = tz.localize(datetime(previous_day.year, previous_day.month, previous_day.day, 23, 59, 59))

    return int(start_of_day.timestamp()), int(end_of_day.timestamp())


# Функция для получения сообщений за сутки
def get_messages_for_day(peer_id, start_time, end_time):
    messages = []
    offset = 0
    count = 200  # Максимум сообщений за один запрос

    while True:
        response = vk.messages.getHistory(
            peer_id=peer_id,
            count=count,
            offset=offset
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
    user_info = vk.users.get(user_ids=user_id)[0]
    return f"{user_info['first_name']} {user_info['last_name']}"


# Функция отправки отчета
def send_report():
    # Получение сообщений за прошедшие сутки
    start_time, end_time = get_unix_time_range()
    messages = get_messages_for_day(peer_id, start_time, end_time)

    people_dict = dict()
    people_messages_dict = dict()
    messages_list = list()
    # Вывод сообщений с именами авторов


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

    mas_for_message_string = list()

    id_name_dict = dict()
    for msg in messages:
        if msg['from_id'] not in id_name_dict:
            id_name_dict[msg['from_id']] = get_user_name(msg['from_id'])

    for msg in messages:
        author_name = msg['from_id']
        # print(f"[{date}] Автор: {author_name}, Текст: {msg['text']}")
        if len(msg['text'].split(" ")) < 150:
            messages_list.append(msg['text'])
        if "Всего сообщений за день - " not in msg['text']:
            mas_for_message_string.append(id_name_dict[author_name] + ": " + msg['text'] + "\n")
        if author_name not in people_dict:
            people_dict[author_name] = 1
            people_messages_dict[author_name] = list()
            if len(msg['text'].split(" ")) < 150:
                people_messages_dict[author_name].append(msg['text'])
        else:
            people_dict[author_name] += 1
            if len(msg['text'].split(" ")) < 150:
                people_messages_dict[author_name].append(msg['text'])

    dict_lemma = create_frequency_dict_lemma(" ".join(messages_list))
    dict_lemma_top10 = dict(sorted(dict_lemma.items(), key=lambda item: item[1], reverse=True)[:10])
    top_10_string = "\n".join([f"{word}: {count}" for word, count in dict_lemma_top10.items()])

    gptAnswer = getAnswer("Расскажи о лучших блюдах в китае")
    for i in mas_for_message_string[::-1]:
        message_string += i
    gptAnswer = getAnswer(message_string)

    total_sum = sum(people_dict.values())
    sorted_people_dict = sorted(people_dict.items(), key=lambda item: item[1], reverse=True)

    response_message = ""
    mat_count = 0
    for i in messages_list:
        response_message = ("На каждой из следующих строк - сообщения. Тебе нужно посчитать кол-во сообщений, в которых может "
                            "присутствовать мат в той или иной форме. В ответ выведи только число\n")
        response_message += i + "\n"
        if findMat(i):
            mat_count += 1
    try:
        mat_count = max(mat_count, int(str(getAnswer(response_message)['choices'][0]['message']['content'])))  # Пробуем распарсить значение
    except Exception:
        mat_count = mat_count

    top10_count_messages = sorted_people_dict[:5]
    top10_words_count = return_words_dict(people_messages_dict)
    output_str = (
            "Всего сообщений за день - " + str(total_sum) +
            "\nИз них с матами - " + str(mat_count) +
            "\n\nТоп 5 по кол-ву сообщений:\n\n" +
            "\n".join([f"{i + 1}) {get_user_name(item[0])}: {item[1]} сообщений" for i, item in
                       enumerate(top10_count_messages)]) +
            "\n\nТоп 5 по словам:\n\n" +
            "\n".join([f"{i + 1}) {get_user_name(user)}: {count} слов" for i, (user, count) in
                       enumerate(top10_words_count.items())][:5])
            + "\n\nТоп 10 слов за день:\n\n" + top_10_string
            + "\n\nКраткий пересказ, о чем говорили за день:\n\n" + str(gptAnswer['choices'][0]['message']['content'])
    )

    print(output_str)
    vk.messages.send(peer_id=peer_id, message=output_str, random_id=int(time.time()))


# Функция для ожидания 5:37 по локальному времени
def wait_until_537():
    tz = pytz.timezone('Asia/Yekaterinburg')
    now = datetime.now(tz)
    target_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if now > target_time:
        target_time += timedelta(days=1)

    time_to_wait = (target_time - now).total_seconds()
    # print(f"Ожидаю {time_to_wait} секунд до 5:37...")
    time.sleep(time_to_wait)


def return_words_dict(words_dict):
    return_dict = dict()
    for key, phrases in words_dict.items():
        total_words = sum(len(phrase.split()) for phrase in phrases)
        return_dict[key] = total_words
    return dict(sorted(return_dict.items(), key=lambda item: item[1], reverse=True)[:10])


# Основной цикл
while True:
    wait_until_537()  # Ждем до 5:37
    send_report()  # Отправляем отчет
