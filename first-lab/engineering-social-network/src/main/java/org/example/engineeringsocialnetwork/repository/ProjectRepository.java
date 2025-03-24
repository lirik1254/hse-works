package org.example.engineeringsocialnetwork.repository;

import org.example.engineeringsocialnetwork.entities.Project;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProjectRepository extends JpaRepository<Project, Long> {
}
