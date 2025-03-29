# Было сделано
1. Настроен CI-процесс для распределенной системы. Тесты не поделил на юнит/интеграционные, потому что у меня все тесты интеграционные.
![image](https://github.com/user-attachments/assets/8d4dcee2-74c1-4ec8-9fc7-dcc99e1d5db2)

2. Было произведено кеширование данных из СУБД. При каждом get запросе проверяется, есть ли данные в redis. Если нет - данные берутся из СУБД и записываются в redis. Если есть - выводятся данные из redis. TTL - 10 секунд.
![image](https://github.com/user-attachments/assets/24da1175-0769-417c-8ce5-c5bb538fea9b)
![image](https://github.com/user-attachments/assets/caea7266-3626-426a-99ce-5672779a3b98)

3. Был настроен Graylog - каждый из 3 микросервисов присылает логи в одно хранилище Graylog
![image](https://github.com/user-attachments/assets/125278b9-829f-4083-8848-c37ea7c60f6d)

4. Были обновлены интеграционные тесты с учетом наличия редис (с использованием Testcontainers). Также был обновлён код (добавлен редис для кеширования get-запросов). Ну и в завершение в docker-compose файл добавлен graylog и redis.
![image](https://github.com/user-attachments/assets/f1807343-31f5-4876-9974-7e93462ca033)
![image](https://github.com/user-attachments/assets/f34bee4d-85d3-4067-886d-de493be8beda)
![image](https://github.com/user-attachments/assets/6a297df5-58dc-41c9-83c3-24fb5861a351)
![image](https://github.com/user-attachments/assets/6b10c38c-d88e-4174-8085-e38e8a5b06a2)



Успешная работа продемонстрирована ниже

![image](https://github.com/user-attachments/assets/a23fb3eb-92c2-4b7a-9fe2-2ea88701f7f0)

из Redis в среднем 7 мс 

![image](https://github.com/user-attachments/assets/b536feb2-8eb4-4ee5-99a8-0d1edaa35d3b)

из БД 11 мс 

![image](https://github.com/user-attachments/assets/e2acb7cf-7f66-4e8e-818d-04adec0909da)

При увеличении объёма данных разница будет более существенной.

Отвечая на вопрос, что делать, если со временем  ключ из кеша станем получать слишком долго, можно привести следующие стратегии:
- Грамотно произвести настройку TTL. Если у нас обновляются данные каждые 10 мс, то вряд ли стоит использовать редис.
- Разделить данные между несколькими нодами (Redis Cluster)
- Сжатие данных
- Размещение кеша как можно ближе к приложению
