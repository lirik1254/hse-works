package backend.academy.course;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@Slf4j
public class CourseApplication {

    public static void main(String[] args) {
        log.info("application started");
        SpringApplication.run(CourseApplication.class, args);
    }

}
