package org.example.engineeringsocialnetwork;

import org.example.engineeringsocialnetwork.controller.UserController;
import org.example.engineeringsocialnetwork.entities.Users;
import org.example.engineeringsocialnetwork.services.UserService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

public class UserControllerTest {

    @InjectMocks
    private UserController userController;

    @Mock
    private UserService userService;

    private Users testUser;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        testUser = new Users(1L, 52, "laskdjf", "alksjdf", "lajsdf", LocalDate.of(2020,10,10), null);
    }

    @Test
    void testGetAllUsers() throws Exception {
        when(userService.getAllUsers()).thenReturn(CompletableFuture.completedFuture(List.of(testUser)));

        var result = userController.getAllUsers();

        assertNotNull(result);
        assertFalse(result.isEmpty());
        assertEquals(1, result.size());
    }

    @Test
    void testGetUserById() throws Exception {
        when(userService.getUserById(1L)).thenReturn(CompletableFuture.completedFuture(Optional.of(testUser)));

        var result = userController.getUserById(1L);

        assertTrue(result.isPresent());
        assertEquals(testUser, result.get());
    }

    @Test
    void testAddUser() throws Exception {
        when(userService.addUser(any(Users.class))).thenReturn(CompletableFuture.completedFuture(testUser));

        var result = userController.addUser(testUser);

        assertNotNull(result);
        assertEquals(testUser, result);
    }

    @Test
    void testUpdateUser() throws Exception {
        when(userService.updateUser(any(Users.class))).thenReturn(CompletableFuture.completedFuture(testUser));

        var result = userController.updateUser(testUser);

        assertNotNull(result);
        assertEquals(testUser, result);
    }

    @Test
    void testDeleteUser() throws Exception {
        when(userService.deleteUser(1L)).thenReturn(CompletableFuture.completedFuture(null));

        assertDoesNotThrow(() -> userController.deleteUser(1L));
    }
}
