package backend.academy.user.service;

import backend.academy.user.dto.CreateUserCommand;
import backend.academy.user.model.CourseUser;
import backend.academy.user.model.Users;
import backend.academy.user.repository.CourseUserRepository;
import backend.academy.user.repository.UserRepository;
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

@SuppressWarnings({"ImportOrder", "MagicNumber"})
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {
    private static final String ALL_USERS = "allUsers";
    private final UserRepository userRepository;
    private final CourseUserRepository courseUserRepository;
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final RedisTemplate<String, Object> redisTemplate;

    @Transactional
    @Async
    public CompletableFuture<Users> createUser(CreateUserCommand command) {
        Users user = new Users();
        user.setName(command.getName());
        user.setEmail(command.getEmail());

        Users savedUser = userRepository.save(user);

        kafkaTemplate.send("user", savedUser.getId().toString());
        return CompletableFuture.completedFuture(user);
    }

    @Transactional
    @Async
    public void enrollUserToCourse(Long userId, Long courseId) {
        CourseUser courseUser = new CourseUser();
        courseUser.setUserId(userId);
        courseUser.setCourseId(courseId);
        courseUserRepository.save(courseUser);
    }

    @Transactional
    @Async
    public CompletableFuture<List<Users>> getAllUsers() {
        ValueOperations<String, Object> valueOps = redisTemplate.opsForValue();
        List<Users> allUsers = (List<Users>) valueOps.get(ALL_USERS);

        if (allUsers != null) {
            log.info("get users from redis");
            return CompletableFuture.completedFuture(allUsers);
        }
        log.info("get users from DB");
        allUsers = userRepository.findAll();
        valueOps.set(ALL_USERS, allUsers, 10, TimeUnit.SECONDS);

        return CompletableFuture.completedFuture(allUsers);
    }
}
