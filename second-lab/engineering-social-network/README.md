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