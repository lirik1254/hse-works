package backend.academy.user;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class KafkaConsumer {

    @KafkaListener(topics = "course", groupId = "course_consumer")
    public void listenUser(String message) {
        Long courseId = Long.parseLong(message.split(" ")[0]);
        String content = message.split(" ", 2)[1];

        log.info("Создался курс с id:{} и content:{}. Возможно, стоит добавить"
                + " всем пользователям этот курс или другую логику", courseId, content);
    }
}
