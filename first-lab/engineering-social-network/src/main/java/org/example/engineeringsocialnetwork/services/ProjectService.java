package org.example.engineeringsocialnetwork.services;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import lombok.extern.slf4j.Slf4j;
import org.example.engineeringsocialnetwork.DTO.ProjectDTO;
import org.example.engineeringsocialnetwork.entities.Project;
import org.example.engineeringsocialnetwork.entities.Users;
import org.example.engineeringsocialnetwork.repository.ProjectRepository;
import org.example.engineeringsocialnetwork.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;



@Service
@Slf4j
public class ProjectService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @Async
    public CompletableFuture<List<Project>> getAllProjects() {
        return CompletableFuture.completedFuture(projectRepository.findAll());
    }

    @Async
    public CompletableFuture<Optional<Project>> getProjectById(Long id) {
        return CompletableFuture.completedFuture(projectRepository.findById(id));
    }

    @Async
    public CompletableFuture<Project> addProject(ProjectDTO projectDTO) {
        Users user = userRepository.findById(projectDTO.userId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        Project project = new Project();
        project.setTitle(projectDTO.title());
        project.setDescription(projectDTO.description());
        project.setUser(user);

        return CompletableFuture.completedFuture(projectRepository.save(project));
    }

    @Async
    public CompletableFuture<Project> updateProject(Project project) {
        return CompletableFuture.completedFuture(projectRepository.save(project));
    }

    @Async
    public CompletableFuture<Void> deleteProject(Long id) {
        projectRepository.deleteById(id);
        return CompletableFuture.completedFuture(null);
    }
}
