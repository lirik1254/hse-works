package backend.academy.user.service;

import backend.academy.user.dto.CreateUserCommand;
import backend.academy.user.model.CourseUser;
import backend.academy.user.model.Users;
import backend.academy.user.repository.CourseUserRepository;
import backend.academy.user.repository.UserRepository;
import jakarta.transaction.Transactional;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final CourseUserRepository courseUserRepository;
    private final KafkaTemplate<String, String> kafkaTemplate;

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
        return CompletableFuture.completedFuture(userRepository.findAll());
    }
}
