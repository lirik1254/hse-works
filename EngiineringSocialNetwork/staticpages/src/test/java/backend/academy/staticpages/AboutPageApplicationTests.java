package backend.academy.staticpages;

import backend.academy.staticpages.entity.AboutPage;
import backend.academy.staticpages.repository.AboutPageRepository;
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
import java.util.concurrent.TimeUnit;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@AutoConfigureMockMvc
@SpringBootTest
@Testcontainers
class AboutPageApplicationTests {

    @Container
    public static final PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:17");

    @Container
    public static final KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("apache/kafka:3.7.0"));

    @Autowired
    MockMvc mockMvc;

    @Autowired
    public AboutPageRepository aboutPageRepository;

    @Autowired
    public CoursePageRepository coursePageRepository;

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @MockitoSpyBean
    private KafkaConsumer kafkaConsumer;

    @Captor
    private ArgumentCaptor<String> messageCaptor;

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }

    @BeforeEach
    public void setUp() {
        aboutPageRepository.deleteAll();
        aboutPageRepository.resetSequence();
    }


    @DisplayName("Создание AboutPage")
    @Test
    public void test3() throws Exception {
        String content = "content about page with 1 num";

        mockMvc.perform(post("/about-pages/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(content))
                .andExpect(status().isOk());

        Thread.sleep(1000);

        List<AboutPage> aboutPages = aboutPageRepository.findAll();

        Assertions.assertEquals(1, aboutPages.size());
        Assertions.assertEquals(content, aboutPages.get(0).getContent());
    }

    @DisplayName("Получение AboutPage по Id")
    @Test
    public void test4() throws Exception {
        String content = "О пользаке 1 страница";

        AboutPage aboutPage = new AboutPage();
        aboutPage.setContent(content);
        aboutPage.setUserId(52L);
        aboutPageRepository.save(aboutPage);

        mockMvc.perform(get("/about-pages/52"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.userId").value(52))
                .andExpect(jsonPath("$.content").value(content));
    }

    @DisplayName("Получение всех AboutPage если их нет")
    @Test
    public void test5() throws Exception {
        mockMvc.perform(get("/about-pages"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$.length()").value(0));
    }

    @DisplayName("Получение всех AboutPage если они есть")
    @Test
    public void test6() throws Exception {
        String content = "Страница о пользователе 52";

        AboutPage aboutPage = new AboutPage();
        aboutPage.setUserId(52L);
        aboutPage.setContent(content);

        aboutPageRepository.save(aboutPage);

        mockMvc.perform(get("/about-pages"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].userId").value(52))
                .andExpect(jsonPath("$[0].content").value(content));
    }

    @DisplayName("При получении сообщения в топик user, создаётся страница для user'а")
    @Test
    public void test7() throws Exception {
        String userId = "1";
        Thread.sleep(1000);
        kafkaTemplate.send("user", userId);

        Awaitility.await()
                .atMost(10, TimeUnit.SECONDS)
                .untilAsserted(() -> {
                    verify(kafkaConsumer).listenUser(messageCaptor.capture());
                    Assertions.assertEquals(userId, messageCaptor.getValue());
                });

        mockMvc.perform(get("/about-pages/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.userId").value(1))
                .andExpect(jsonPath("$.content").value("AboutUserWithId 1 page"));
    }

}
