from VKInteraction import send_report, PEER_ID
from TimeUtils import wait_until

# Чтобы протестить работу, поставь время на 1 минуту больше текущего и id в send_report укажи для избранного
# Ожидание отправки ~ 5 минут. Чтобы проверить, что он реально чето делает, поставь брейкпоинт в методе get_user_name
while True:
    wait_until(0, 0, 0)
    send_report(PEER_ID)
