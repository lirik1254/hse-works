# Развертывание

1. Установить `Docker` и `Docker Compose`. [Инструкция](https://docs.docker.com/compose/install/)
2. В папке `envs` создать файл `.env.prod` и заполнить его переменными окружения
3. Выполнить команду `docker-compose up --build -d`, находясь в папке `deploy/prod`