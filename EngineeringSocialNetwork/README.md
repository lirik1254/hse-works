## EngineeringSocialNetwork 

### Все команды выполняются в корне проекта

Запуск линтеров

```shell
mvn checkstyle:check
```

Билд проекта + запуск тестов (обязательно должен быть запущен докер)
```shell
mvn clean install
```

Запуск проекта через докер 
```shell
docker-compose up --build
```

Не забудьте указать GRAYLOG_ROOT_PASSWORD_SHA2 и GRAYLOG_PASSWORD_SECRET в .env файле (если его сейчас нет).
Если есть, то пароль и логин - admin 

Также после запуска необходимо авторизоваться в GrayLog и указать Input (GELF UDP)