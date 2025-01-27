from datetime import datetime
from .output_utils import pluralize_days, pluralize_hours


def get_last_seen_time(last_online_time_seconds):
    """
    Сколько часов дней и часов назад был в сети пользователь
    """
    current_timestamp = datetime.now().timestamp()

    time_difference = current_timestamp - last_online_time_seconds

    if time_difference >= 86400:
        days = int(time_difference // 86400)
        hours = int((time_difference % 86400) // 3600)
        return f"Был в сети  {pluralize_days(days)} {pluralize_hours(hours)} назад"
    else:
        hours = int(time_difference // 3600)
        return f"Был в сети {pluralize_hours(hours)} назад"


def get_registration_time(registration_seconds):
    """
    Дата регистрации
    """
    dt_object = datetime.fromtimestamp(registration_seconds)
    formatted_date = dt_object.strftime("%d-%m-%Y %H:%M")
    return formatted_date
