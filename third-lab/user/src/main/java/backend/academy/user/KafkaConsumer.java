package backend.academy.user;

import java.util.Arrays;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class KafkaConsumer {

    @KafkaListener(topics = "course", groupId = "course_consumer1")
    public void listenUser(String message) {
        String[] parts = message.split(" ");
        Long courseId = Long.parseLong(parts[0]);

        String content = String.join(" ", Arrays.copyOfRange(parts, 1, parts.length));

        log.info("Создался курс с id:{} и content:{}. Возможно, стоит добавить"
                + " всем пользователям этот курс или другую логику", courseId, content);
    }
}
