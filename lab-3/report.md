# 1 Добавить ранее созданные или создать диаграммы контейнеров и компонентов нотации C4 model. 


## Диаграмма контейнеров
![Контейнеры](https://github.com/user-attachments/assets/6670f1d2-8f60-4e82-bf86-741a1f284742)

## Диаграмма компонентов для системы загрузки видео
![Контейнер для системы загрузки видео](https://github.com/user-attachments/assets/29faea55-6e2c-41b0-89ab-3b9153626f5b)


# 2 Построить диаграмму последовательностей для выбранного варианта использования
![Диаграмма последовательностей](https://github.com/user-attachments/assets/84418f0c-bc61-4512-aa9d-906e11e7ec26)



# 3 Построить модель БД

![3 Модель БД Untitled](https://github.com/user-attachments/assets/16f98e50-5b37-4022-bcda-afd017ed906c)

# 4 Реализовать требуемый клиентский и серверный код с учетом принципов KISS, YAGNI, DRY и SOLID. Пояснить, каким образом были учтены эти принципы. 

``` java
package com.example.demo;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
class Video {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;                // Уникальный идентификатор
    private String title;           // Название
    private String description;     // Описание
    private String fileUrl;         // Ссылка на файл

    public Video(String title, String description, String fileUrl) {
        this.title = title;
        this.description = description;
        this.fileUrl = fileUrl;
    }
}

package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/videos")
class VideoController {

    private final VideoService videoService;

    @Autowired
    public VideoController(VideoService videoService) {
        this.videoService = videoService;
    }

    @PostMapping
    public ResponseEntity<String> uploadVideo(@RequestBody VideoRequest request) {
        videoService.saveVideo(request);
        return ResponseEntity.ok("Видео загружено");
    }

    @GetMapping
    public ResponseEntity<List<Video>> getAllVideos() {
        return ResponseEntity.ok(videoService.getAllVideos());
    }
}

package com.example.demo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
interface VideoRepository extends JpaRepository<Video, Long> {}

package com.example.demo;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
class VideoRequest {
    private String title;
    private String description;
    private String fileUrl;
}

package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
class VideoService {

    private final VideoRepository videoRepository;

    @Autowired
    public VideoService(VideoRepository videoRepository) {
        this.videoRepository = videoRepository;
    }

    @Transactional
    public void saveVideo(VideoRequest request) {
        Video video = new Video(request.getTitle(), request.getDescription(), request.getFileUrl());
        videoRepository.save(video);
    }

    public List<Video> getAllVideos() {
        return videoRepository.findAll();
    }
}

package com.example.demo;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
class VideoRequest {
    private String title;
    private String description;
    private String fileUrl;
}
```

### KISS
Код простой и понятный. Все классы выполняют строго определенные задачи
Используются стандартные практики Spring Framework

### YAGNI
Ненужный код отсутствует, все реализованные методы и классы нужны для выполнения текущей функциональности.

Не вижу смысла уточнять на конкретном примере принцип, который говорит "тебе это не нужно". 
Вот сравнительная таблица, почему используются те или иные классы 

| **Класс**          | **Обязателен?** | **Обоснование**                                                                  |
|---------------------|-----------------|-----------------------------------------------------------------------------------|
| `Video`            | Да              | Представляет сущность видео в базе данных.                                       |
| `VideoRequest`     | Нет, но полезен | Обеспечивает разделение данных DTO и сущности, улучшает читаемость и расширяемость. |
| `VideoController`  | Да              | Обрабатывает запросы, связывает сервис и клиент.                                 |
| `VideoService`     | Нет, но полезен | Упрощает контроллер, выделяет бизнес-логику, делает код гибким.                  |
| `VideoRepository`  | Да              | Обеспечивает доступ к базе данных.                                               |


### DRY
Код не содержит дублирования.
Маппинг между VideoRequest и Video вынесен в метод сервиса, что исключает повторяющийся код.

### SOLID

Single Responsibility (Принцип единственной ответственности):

Каждый класс отвечает за свою задачу:
VideoController — управление запросами.
VideoService — бизнес-логика.
VideoRepository — доступ к данным.
VideoRequest — DTO для передачи данных.
Это соответствует SRP.

Open-Closed (Принцип открытости/закрытости):
Логика в сервисе легко расширяется, например, можно добавить обработку ошибок или новую бизнес-логику, не изменяя контроллер.

Liskov Substitution (Принцип подстановки Барбары Лисков):
Все интерфейсы и классы могут быть заменены их реализациями без изменения внешнего поведения.

В данный момент VideoRepository реализует интерфейс JpaRepository<Video, Long> предоставляя готовую функциональность для работы с базой данных. 
Но если мы заменим VideoRepository на другую реализацию интерфейса, допустим CustomVideoRepositor, то код продолжит работать корректно, т.к. CustomVideoRepository соблюдает контракт VideoRepository интерфейса

```
@Service
class VideoService {

    private final VideoRepository videoRepository;

    @Autowired
    public VideoService(CustomVideoRepository customVideoRepository) {
        this.videoRepository = customVideoRepository;
    }

    @Transactional
    public void saveVideo(VideoRequest request) {
        Video video = new Video(request.getTitle(), request.getDescription(), request.getFileUrl());
        videoRepository.save(video);
    }

    public List<Video> getAllVideos() {
        return videoRepository.findAll();
    }
}
```

Interface Segregation (Принцип разделения интерфейса):
Интерфейс VideoRepository достаточно узкий и специфичный.

Dependency Inversion (Принцип инверсии зависимостей):
Сервис использует зависимость от интерфейса VideoRepository, а не конкретной реализации.
