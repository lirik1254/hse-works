package backend.academy.staticpages;

import backend.academy.staticpages.repository.AboutPageRepository;
import backend.academy.staticpages.repository.CoursePageRepository;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.kafka.KafkaContainer;
import org.testcontainers.utility.DockerImageName;

//@SpringBootTest
//@AutoConfigureMockMvc
//@Testcontainers
//public abstract class TestContainersConfigure {
//    @Container
//    protected static final PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:17");
//
//    @Container
//    protected static final KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("apache/kafka:3.7.0"));
//
//    @Autowired
//    MockMvc mockMvc;
//
//    @Autowired
//    protected AboutPageRepository aboutPageRepository;
//
//    @Autowired
//    protected CoursePageRepository coursePageRepository;
//
//    @DynamicPropertySource
//    static void configureProperties(DynamicPropertyRegistry registry) {
//        registry.add("spring.datasource.url", postgres::getJdbcUrl);
//        registry.add("spring.datasource.username", postgres::getUsername);
//        registry.add("spring.datasource.password", postgres::getPassword);
//        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
//    }
//
//
//}
