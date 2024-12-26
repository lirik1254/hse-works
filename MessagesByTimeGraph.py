import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import pytz

# Часовой пояс для Екатеринбурга
tz = pytz.timezone('Asia/Yekaterinburg')

# Функция для извлечения времени из метки и преобразования в локальное время
def convert_timestamp_to_local(timestamp):
    utc_time = datetime.utcfromtimestamp(timestamp)  # Преобразуем UNIX-время в UTC
    utc_time = pytz.utc.localize(utc_time)  # Преобразуем в объект времени UTC
    local_time = utc_time.astimezone(tz)  # Конвертируем в локальное время (Екатеринбург)
    return local_time

# Пример использования
def extract_hour_from_messages(messages):
    hours = []
    for message in messages:
        timestamp = message['date']
        message_time_local = convert_timestamp_to_local(timestamp)
        hours.append(message_time_local.hour)
    return hours


# Функция для создания графика
def plot_messages_by_time(messages):
    # Извлекаем часы из сообщений
    hours = extract_hour_from_messages(messages)

    # Считаем количество сообщений по каждому часу
    hourly_counts = pd.Series(hours).value_counts().sort_index()

    # Строим график
    plt.figure(figsize=(10, 6))
    plt.bar(hourly_counts.index, hourly_counts.values, color='skyblue')
    plt.xlabel('Час дня')
    plt.ylabel('Количество сообщений')
    plt.title('Сообщения по времени суток')
    plt.xticks(range(24))  # Отображаем все часы
    plt.tight_layout()
    plt.savefig('Photo/messages_by_time.png')
    plt.close()