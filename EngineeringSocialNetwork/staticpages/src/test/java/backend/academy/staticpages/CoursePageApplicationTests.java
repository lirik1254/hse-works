package backend.academy.staticpages;

import backend.academy.staticpages.entity.CoursePage;
import backend.academy.staticpages.repository.CoursePageRepository;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;
import org.springframework.test.web.servlet.MockMvc;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.kafka.KafkaContainer;
import org.testcontainers.shaded.org.awaitility.Awaitility;
import org.testcontainers.utility.DockerImageName;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class CoursePageApplicationTests extends TestContainersSetUp{
    @Autowired
    private CoursePageRepository coursePageRepository;

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @MockitoSpyBean
    private KafkaConsumer kafkaConsumer;

    @Captor
    private ArgumentCaptor<String> messageCaptor;

    @BeforeEach
    public void setUp() {
        coursePageRepository.deleteAll();
    }

    @DynamicPropertySource
    static void kafkaProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.consumer.group-id",
                () -> "group-" + UUID.randomUUID());
    }

    @DisplayName("Создание CoursePage")
    @Test
    public void testCreateCoursePage() throws Exception {
        String content = "Course content for course 1";

        mockMvc.perform(post("/course-pages/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(content))
                .andExpect(status().isOk());
        Thread.sleep(1000);

        List<CoursePage> coursePages = coursePageRepository.findAll();

        Assertions.assertEquals(1, coursePages.size());
        Assertions.assertEquals(content, coursePages.get(0).getContent());
        Assertions.assertEquals(1L, coursePages.get(0).getCourseId());
    }

    @DisplayName("Получение CoursePage по courseId")
    @Test
    public void testGetCoursePageById() throws Exception {
        String content = "Advanced Java Course";

        CoursePage coursePage = new CoursePage();
        coursePage.setContent(content);
        coursePage.setCourseId(101L);
        coursePageRepository.save(coursePage);

        mockMvc.perform(get("/course-pages/101"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").exists())
                .andExpect(jsonPath("$.courseId").value(101))
                .andExpect(jsonPath("$.content").value(content));
    }

    @DisplayName("Получение всех CoursePage если их нет")
    @Test
    public void testGetAllCoursePagesEmpty() throws Exception {
        mockMvc.perform(get("/course-pages"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$.length()").value(0));
    }

    @DisplayName("Получение всех CoursePage если они есть")
    @Test
    public void testGetAllCoursePages() throws Exception {
        CoursePage page1 = new CoursePage();
        page1.setCourseId(1L);
        page1.setContent("Content 1");

        CoursePage page2 = new CoursePage();
        page2.setCourseId(2L);
        page2.setContent("Content 2");

        coursePageRepository.saveAll(List.of(page1, page2));

        mockMvc.perform(get("/course-pages"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].courseId").value(1))
                .andExpect(jsonPath("$[1].courseId").value(2));
    }

    @DisplayName("При получении сообщения в топик course, создаётся страница курса")
    @Test
    public void testKafkaCourseMessageProcessing() throws Exception {
        String courseMessage = "2023 Introduction_to_Spring";
        Thread.sleep(1000);
        kafkaTemplate.send("course", courseMessage);

        Awaitility.await()
                .atMost(10, TimeUnit.SECONDS)
                .untilAsserted(() -> {
                    verify(kafkaConsumer).listenCourse(messageCaptor.capture());
                    Assertions.assertEquals(courseMessage, messageCaptor.getValue());
                });

        CoursePage result = coursePageRepository.findCoursePageByCourseId(2023L);
        Assertions.assertNotNull(result);
        Assertions.assertTrue(result.getContent().contains("Introduction_to_Spring"));
    }
}