from VKInteraction import send_report, PEER_ID
from TimeUtils import wait_until


# Основной цикл
while True:
    wait_until(0, 0, 0)
    send_report(PEER_ID)
