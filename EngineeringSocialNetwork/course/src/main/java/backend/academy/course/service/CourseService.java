package backend.academy.course.service;

import backend.academy.course.dto.CreateCourseCommand;
import backend.academy.course.dto.CreateModuleCommand;
import backend.academy.course.model.Course;
import backend.academy.course.model.Lesson;
import backend.academy.course.model.Module;
import backend.academy.course.repository.CourseRepository;
import backend.academy.course.repository.LessonRepository;
import backend.academy.course.repository.ModuleRepository;
import jakarta.transaction.Transactional;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
@SuppressWarnings("MagicNumber")
public class CourseService {
    private static final String ALL_COURSES = "allCourses";
    private final CourseRepository courseRepository;
    private final ModuleRepository moduleRepository;
    private final LessonRepository lessonRepository;
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final RedisTemplate<String, Object> redisTemplate;

    @Transactional
    @Async
    public CompletableFuture<Course> createCourse(CreateCourseCommand command) {
        Course course = new Course();
        course.setName(command.getName());
        course.setDescription(command.getDescription());
        Course savedCourse = courseRepository.save(course);
        kafkaTemplate.send("course", savedCourse.getId() + " "
                + savedCourse.getDescription());
        return CompletableFuture.completedFuture(course);
    }

    @Transactional
    @Async
    public CompletableFuture<Module> createModule(CreateModuleCommand command) {
        // создаем модуль
        Module module = new Module();
        module.setCourseId(command.getCourseId());
        module.setName(command.getName());
        module.setDescription(command.getDescription());
        return CompletableFuture.completedFuture(moduleRepository.save(module));
    }

    @Transactional
    @Async
    public CompletableFuture<Lesson> createLesson(Long moduleId, String title, String content) {
        // создаем урок
        Lesson lesson = new Lesson();
        lesson.setModuleId(moduleId);
        lesson.setTitle(title);
        lesson.setContent(content);
        return CompletableFuture.completedFuture(lessonRepository.save(lesson));
    }

    @Transactional
    @Async
    public CompletableFuture<List<Course>> getAllCourses() {
        ValueOperations<String, Object> valueOps = redisTemplate.opsForValue();
        List<Course> courses = (List<Course>) valueOps.get(ALL_COURSES);

        if (courses != null) {
            log.info("get courses from redis");
            return CompletableFuture.completedFuture(courses);
        }
        log.info("get courses from DB");
        courses = courseRepository.findAll();
        valueOps.set(ALL_COURSES, courses, 10, TimeUnit.SECONDS);
        return CompletableFuture.completedFuture(courses);
    }
}
