import os

from celery import Celery

# Указываем правильный путь к настройкам Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algopath.settings')  # Замените 'algopath.settings' на имя вашего проекта
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('algopath')

# Автоматически настраивает Celery с использованием настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Ожидает, что задачи будут автоматически обнаружены в проекте
app.autodiscover_tasks()