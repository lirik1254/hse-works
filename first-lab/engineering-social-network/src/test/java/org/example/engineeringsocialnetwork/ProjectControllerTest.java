package org.example.engineeringsocialnetwork;

import org.example.engineeringsocialnetwork.DTO.ProjectDTO;
import org.example.engineeringsocialnetwork.controller.ProjectController;
import org.example.engineeringsocialnetwork.entities.Project;
import org.example.engineeringsocialnetwork.entities.Users;
import org.example.engineeringsocialnetwork.repository.UserRepository;
import org.example.engineeringsocialnetwork.services.ProjectService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.when;
import static org.junit.jupiter.api.Assertions.*;

class ProjectControllerTest {

    @InjectMocks
    private ProjectController projectController;

    @Mock
    private ProjectService projectService;

    private Project testProject;
    private Users testUser;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        testUser = new Users(1L, 50, "alskdjf", "alskjdf", "laksjdf", LocalDate.of(2000, 10, 10), null);
        testProject = new Project(1L, "Test Project", "Description", testUser);
    }

    @Test
    void testGetAllProjects() throws Exception {
        when(projectService.getAllProjects()).thenReturn(CompletableFuture.completedFuture(List.of(testProject)));

        var result = projectController.getAllProjects();

        assertNotNull(result);
        assertFalse(result.isEmpty());
        assertEquals(1, result.size());
    }

    @Test
    void testGetProjectById() throws Exception {
        when(projectService.getProjectById(1L)).thenReturn(CompletableFuture.completedFuture(Optional.of(testProject)));

        var result = projectController.getProjectById(1L);

        assertTrue(result.isPresent());
        assertEquals(testProject, result.get());
    }

    @Test
    void testAddProject() throws Exception {
        ProjectDTO projectDTO = new ProjectDTO("Test Project", "Description", 1L);
        when(projectService.addProject(any(ProjectDTO.class))).thenReturn(CompletableFuture.completedFuture(testProject));

        var result = projectController.addProject(projectDTO);

        assertNotNull(result);
        assertEquals(testProject, result);
    }

    @Test
    void testUpdateProject() throws Exception {
        when(projectService.updateProject(any(Project.class))).thenReturn(CompletableFuture.completedFuture(testProject));

        var result = projectController.updateProject(testProject);

        assertNotNull(result);
        assertEquals(testProject, result);
    }

    @Test
    void testDeleteProject() throws Exception {
        when(projectService.deleteProject(anyLong())).thenReturn(CompletableFuture.completedFuture(null));

        assertDoesNotThrow(() -> projectController.deleteProject(1L));
    }
}
