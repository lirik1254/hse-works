from VKInteraction import send_report
from Utils.TimeUtils import wait_until

# Чтобы протестить работу, поставь время на 1 минуту больше текущего и id в send_report укажи для избранного
# Ожидание отправки ~ 2 минуты. Чтобы проверить, что он реально чето делает, поставь брейкпоинт в методе get_user_name
while True:
    wait_until(6, 21, 0)
    send_report(181507171)
    print("Сообщение отправлено")
