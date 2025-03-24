package org.example.engineeringsocialnetwork.controller;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import lombok.extern.slf4j.Slf4j;
import org.example.engineeringsocialnetwork.DTO.ProjectDTO;
import org.example.engineeringsocialnetwork.entities.Project;
import org.example.engineeringsocialnetwork.repository.UserRepository;
import org.example.engineeringsocialnetwork.services.ProjectService;
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
@RequestMapping("/projects")
@Slf4j
public class ProjectController {
    @Autowired
    private ProjectService projectService;

    @Autowired
    private UserRepository userRepository;

    @GetMapping
    public CompletableFuture<List<Project>> getAllProjects() throws ExecutionException, InterruptedException {
        log.info("Получение всех проектов");
        return projectService.getAllProjects();
    }

    @GetMapping("/{id}")
    public Optional<Project> getProjectById(@PathVariable Long id) throws ExecutionException, InterruptedException {
        log.info("Получение проекта по id");
        return projectService.getProjectById(id).get();
    }

    @PostMapping
    public Project addProject(@RequestBody ProjectDTO projectDTO) throws ExecutionException, InterruptedException {
        log.info("Добавление проекта");
        return projectService.addProject(projectDTO).get();
    }

    @PutMapping
    public Project updateProject(@RequestBody Project project) throws ExecutionException, InterruptedException {
        log.info("Обновление проекта");
        return projectService.updateProject(project).get();
    }

    @DeleteMapping("/{id}")
    public void deleteProject(@PathVariable Long id) throws ExecutionException, InterruptedException {
        log.info("Удаление проекта по id");
        projectService.deleteProject(id).get();
    }
}
