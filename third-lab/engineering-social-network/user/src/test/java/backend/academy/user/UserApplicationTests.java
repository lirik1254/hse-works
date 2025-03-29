package backend.academy.user;

import backend.academy.user.model.CourseUser;
import backend.academy.user.model.Users;
import backend.academy.user.repository.CourseUserRepository;
import backend.academy.user.repository.UserRepository;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.awaitility.Awaitility;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;
import org.springframework.test.web.servlet.MockMvc;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.kafka.KafkaContainer;
import org.testcontainers.utility.DockerImageName;

import java.time.Duration;
import java.util.Collections;
import java.util.List;
import java.util.Properties;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.awaitility.Awaitility.await;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@AutoConfigureMockMvc
@SpringBootTest
@Testcontainers
public class UserApplicationTests {

    @Container
    public static GenericContainer<?> redisContainer =
            new GenericContainer<>("redis:7.2-alpine")
                    .withExposedPorts(6379);

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @Container
    public static final PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:17");

    @Container
    public static final KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("apache/kafka:3.7.0"));

    @Autowired
    MockMvc mockMvc;

    // Динамически подставляем параметры подключения
    @DynamicPropertySource
    static void redisProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.redis.host", () -> "localhost");
        registry.add("spring.data.redis.port", () -> redisContainer.getMappedPort(6379));
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }

    @BeforeEach
    void cleanRedis() {
        // Очистка через RedisTemplate
        redisTemplate.getConnectionFactory()
                .getConnection()
                .serverCommands()
                .flushAll();
        courseUserRepository.deleteAll();
        userRepository.deleteAll();
    }

    @DynamicPropertySource
    static void kafkaProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.consumer.group-id",
                () -> "group-" + UUID.randomUUID());
    }

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private CourseUserRepository courseUserRepository;

    @MockitoSpyBean
    private backend.academy.user.KafkaConsumer kafkaConsumer;

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @Captor
    private ArgumentCaptor<String> messageCaptor;

    @DisplayName("Создание пользователя")
    @Test
    public void test1() throws Exception {
        String createString = """
                {
                    "name": "52_Kirillchik_52",
                    "email": "kirill_shulzhik@mail.ru"
                }""";

        mockMvc.perform(post("/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(createString))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))  // Проверка, что в ответе есть поле id
                .andExpect(jsonPath("$.name").value("52_Kirillchik_52"))  // Проверка, что name совпадает
                .andExpect(jsonPath("$.email").value("kirill_shulzhik@mail.ru"));

        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafka.getBootstrapServers());
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "test-group");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList("user"));

            await()
                    .atMost(10, TimeUnit.SECONDS)
                    .untilAsserted(() -> {
                        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                        assertEquals(1, records.count());
                        records.forEach(record -> {
                            assertEquals("1", record.value());
                        });
                    });
        }

    }

    @DisplayName("Получение всех пользователей когда их нет")
    @Test
    public void test2() throws Exception {
        mockMvc.perform(get("/users"))
                .andExpect(status().isOk()) // Проверяем, что статус 200
                .andExpect(jsonPath("$").isArray()) // Проверяем, что ответ — это массив
                .andExpect(jsonPath("$.length()").value(0));

    }

    @DisplayName("Получение всех пользователей когда они есть")
    @Test
    public void test3() throws Exception {
        Users user = new Users();
        user.setName("alblack");
        user.setEmail("52");
        userRepository.save(user);

        mockMvc.perform(get("/users"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].name").value("alblack"))
                .andExpect(jsonPath("$[0].email").value("52"));
    }

    @DisplayName("Тестирование записи студента на курс")
    @Test
    public void test4() throws Exception {
        Users user = new Users();
        user.setName("kirill");
        user.setEmail("kirillchik52@mail.ru");
        userRepository.save(user);

        mockMvc.perform(post("/users/1/enroll/52"))
                .andExpect(status().isOk());

        List<CourseUser> courseUsers = courseUserRepository.findAll();
        assertFalse(courseUsers.isEmpty());
        assertEquals(1, courseUsers.getFirst().getUserId());
        assertEquals(52, courseUsers.getFirst().getCourseId());
    }

    @DisplayName("Получение сообщения из KafkaConsumer")
    @Test
    public void test5() {
        String message = "someMessageToCourseTopic";
        kafkaTemplate.send("course", message);

        await().atMost(10, TimeUnit.SECONDS).untilAsserted(()-> {
            verify(kafkaConsumer).listenUser(messageCaptor.capture());

            String receivedMessage = messageCaptor.getValue();
            assertEquals(message, receivedMessage);
        });
    }
}
