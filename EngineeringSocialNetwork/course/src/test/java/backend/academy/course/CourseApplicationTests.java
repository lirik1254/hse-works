package backend.academy.course;

import backend.academy.course.model.Course;
import backend.academy.course.model.Lesson;
import backend.academy.course.model.Module;
import backend.academy.course.repository.CourseRepository;
import backend.academy.course.repository.LessonRepository;
import backend.academy.course.repository.ModuleRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;
import org.springframework.test.web.servlet.MockMvc;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.kafka.KafkaContainer;
import org.testcontainers.shaded.org.awaitility.Awaitility;
import org.testcontainers.utility.DockerImageName;

import java.util.List;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@AutoConfigureMockMvc
@SpringBootTest
@Testcontainers
class CourseApplicationTests {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:17");

    @Container
    public static final org.testcontainers.kafka.KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("apache/kafka:3.7.0"));

    @Autowired
    MockMvc mockMvc;

    @Autowired
    CourseRepository courseRepository;

    @Autowired
    ModuleRepository moduleRepository;

    @Autowired
    LessonRepository lessonRepository;

    @MockitoBean
    KafkaTemplate<String, String> kafkaTemplate;

    ArgumentCaptor<String> messageCaptor = ArgumentCaptor.forClass(String.class);

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }

    @BeforeEach
    void cleanUp() {
        courseRepository.deleteAll();
        moduleRepository.deleteAll();
        lessonRepository.deleteAll();
    }

    @Test
    @DisplayName("Создание курса и отправка сообщения в Kafka")
    void createCourseWithKafkaTest() throws Exception {
        mockMvc.perform(post("/courses")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"Kafka Course\",\"description\":\"Kafka Desc\"}"))
                .andExpect(status().isOk());

        ArgumentCaptor<String> messageCaptor = ArgumentCaptor.forClass(String.class);
        verify(kafkaTemplate).send(eq("course"), messageCaptor.capture());

        String sentMessage = messageCaptor.getValue();
        assertTrue(sentMessage.matches("\\d+ Kafka Desc"));
    }

    @Test
    @DisplayName("Создание модуля для курса")
    void createModuleTest() throws Exception {
        Course course = courseRepository.save(new Course(null, "Course", "Desc"));

        mockMvc.perform(post("/courses/module")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(String.format("{\"courseId\":%d,\"name\":\"Module 1\",\"description\":\"First module\"}", course.getId())))
                .andExpect(status().isOk());

        List<Module> modules = moduleRepository.findAll();
        assertEquals(1, modules.size());
        assertEquals(course.getId(), modules.get(0).getCourseId());
    }

    @Test
    @DisplayName("Создание урока для модуля")
    void createLessonTest() throws Exception {
        Module module = moduleRepository.save(new Module(null, 1L, "Module", "Desc"));

        mockMvc.perform(post("/courses/module/" + module.getId() + "/lesson")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"title\":\"Lesson 1\",\"content\":\"Content\"}"))
                .andExpect(status().isOk());

        List<Lesson> lessons = lessonRepository.findAll();
        assertEquals(1, lessons.size());
        assertEquals(module.getId(), lessons.get(0).getModuleId());
    }

    @Test
    @DisplayName("Получение всех курсов")
    void getAllCoursesTest() throws Exception {
        courseRepository.saveAll(List.of(
                new Course(null, "Course 1", "Desc1"),
                new Course(null, "Course 2", "Desc2")
        ));

        mockMvc.perform(get("/courses"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].name").value("Course 1"))
                .andExpect(jsonPath("$[1].name").value("Course 2"));
    }
}