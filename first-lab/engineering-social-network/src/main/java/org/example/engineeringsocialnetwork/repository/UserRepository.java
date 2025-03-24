package org.example.engineeringsocialnetwork.repository;

import org.example.engineeringsocialnetwork.entities.Users;
import org.springframework.data.jpa.repository.JpaRepository;


public interface UserRepository extends JpaRepository<Users, Long> {
}
