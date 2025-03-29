package backend.academy.user.controller;

import backend.academy.user.dto.CreateUserCommand;
import backend.academy.user.model.Users;
import backend.academy.user.service.UserService;
import java.util.List;
import java.util.concurrent.ExecutionException;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping
    public Users createUser(@RequestBody CreateUserCommand command) throws ExecutionException, InterruptedException {
        return userService.createUser(command).get();
    }

    @PostMapping("/{userId}/enroll/{courseId}")
    public void enrollUserToCourse(@PathVariable Long userId, @PathVariable Long courseId) {
        userService.enrollUserToCourse(userId, courseId);
    }

    @GetMapping
    public List<Users> getAllUsers() throws ExecutionException, InterruptedException {
        return userService.getAllUsers().get();
    }
}
