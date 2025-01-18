# AlgoPath

## Использование

### Настройки
Переменные окружения находятся в папке `envs`

### Запуск
PROD:
```bash
docker-compose -f deploy/prod/docker-compose.yml up --build -d
````

## Полезные команды для Django

### Управление статическими файлами
Собрать статические файлы:
```bash
python manage.py collectstatic
```

### Управление миграциями
Создать миграции:
```bash
python manage.py makemigrations
```

Применить миграции:
```bash
python manage.py migrate
```

### Управление приложением
Запустить сервер:
```bash
python manage.py runserver 0.0.0.0:8000
```

Проверить наличие ошибок:
```bash
python manage.py check
```

### Управление пользователями
Создать суперпользователя:
```bash
python manage.py createsuperuser
```