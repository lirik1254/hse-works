package backend.academy.staticpages;

import backend.academy.staticpages.service.AboutPageService;
import backend.academy.staticpages.service.CoursePageService;
import java.util.concurrent.ExecutionException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;



@Service
@Slf4j
@RequiredArgsConstructor
public class KafkaConsumer {
    private final AboutPageService aboutPageService;
    private final CoursePageService coursePageService;

    @KafkaListener(topics = "user", groupId = "user_consumer")
    public void listenUser(String message) throws ExecutionException, InterruptedException {
        aboutPageService.createPageByUserId(Long.parseLong(message),
                "AboutUserWithId " + message + " page");
    }

    @KafkaListener(topics = "course", groupId = "course_consumer")
    public void listenCourse(String message) throws ExecutionException, InterruptedException {
        Long courseId = Long.parseLong(message.split(" ")[0]);
        String description = message.split(" ")[1];

        String finalCoursePageContent = """
                Страница курсов\n\nПриветствую тебя на курсе, можешь прочитать описание здесь: \n"""
                + description;
        coursePageService.createPageByCourseId(courseId, finalCoursePageContent);
    }
}
