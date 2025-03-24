package org.example.engineeringsocialnetwork.controller;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutionException;
import lombok.extern.slf4j.Slf4j;
import org.example.engineeringsocialnetwork.entities.Users;
import org.example.engineeringsocialnetwork.services.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/users")
@Slf4j
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping
    public List<Users> getAllUsers() throws ExecutionException, InterruptedException {
        log.info("Получение всех пользователей");
        return userService.getAllUsers().get();  // Получаем результат из CompletableFuture
    }

    @GetMapping("/{id}")
    public Optional<Users> getUserById(@PathVariable Long id) throws ExecutionException, InterruptedException {
        log.info("Получение пользователя по id");
        return userService.getUserById(id).get();  // Получаем результат из CompletableFuture
    }

    @PostMapping
    public Users addUser(@RequestBody Users user) throws ExecutionException, InterruptedException {
        log.info("Добавление пользователя");
        return userService.addUser(user).get();  // Получаем результат из CompletableFuture
    }

    @PutMapping
    public Users updateUser(@RequestBody Users user) throws ExecutionException, InterruptedException {
        log.info("Обновление пользователя");
        return userService.updateUser(user).get();  // Получаем результат из CompletableFuture
    }

    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) throws ExecutionException, InterruptedException {
        log.info("Удаление пользователя по id");
        userService.deleteUser(id).get();  // Получаем результат из CompletableFuture
    }
}
