package org.example.engineeringsocialnetwork.services;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import org.example.engineeringsocialnetwork.entities.Users;
import org.example.engineeringsocialnetwork.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;



@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Async
    public CompletableFuture<List<Users>> getAllUsers() {
        return CompletableFuture.completedFuture(userRepository.findAll());
    }

    @Async
    public CompletableFuture<Optional<Users>> getUserById(Long id) {
        return CompletableFuture.completedFuture(userRepository.findById(id));
    }

    @Async
    public CompletableFuture<Users> addUser(Users user) {
        return CompletableFuture.completedFuture(userRepository.save(user));
    }

    @Async
    public CompletableFuture<Users> updateUser(Users user) {
        return CompletableFuture.completedFuture(userRepository.save(user));
    }

    @Async
    public CompletableFuture<Void> deleteUser(Long id) {
        userRepository.deleteById(id);
        return CompletableFuture.completedFuture(null);
    }
}
