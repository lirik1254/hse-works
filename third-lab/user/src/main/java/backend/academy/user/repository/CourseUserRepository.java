package backend.academy.user.repository;

import backend.academy.user.model.CourseUser;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CourseUserRepository extends JpaRepository<CourseUser, Long> {
}
