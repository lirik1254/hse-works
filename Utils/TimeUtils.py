from datetime import datetime, timedelta
import time
import pytz

# Функция для ожидания определенного времени
def wait_until(hour, minute, second):
    tz = pytz.timezone('Asia/Yekaterinburg')
    now = datetime.now(tz)
    target_time = now.replace(hour = hour, minute = minute, second = second)
    if now > target_time:
        target_time += timedelta(days = 1)
    time_to_wait = (target_time - now).total_seconds()
    # print(f"Ожидаю {time_to_wait} секунд до 5:37...")
    time.sleep(time_to_wait)


# Функция для получения UNIX-времени начала и конца суток прошедших суток
def get_unix_time_range_previous_day():
    # Текущая дата и время с использованием pytz для Yekaterinburg
    tz = pytz.timezone('Asia/Yekaterinburg')
    now = datetime.now(tz)

    # Время начала вчерашнего дня (00:00)
    previous_day = now - timedelta(days=1)

    # Начало и конец предыдущего дня
    start_of_day = tz.localize(datetime(previous_day.year, previous_day.month, previous_day.day, 0, 0, 0))
    end_of_day = tz.localize(datetime(previous_day.year, previous_day.month, previous_day.day, 23, 59, 59))

    return int(start_of_day.timestamp()), int(end_of_day.timestamp())