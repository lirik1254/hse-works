package backend.academy.staticpages.repository;

import backend.academy.staticpages.entity.CoursePage;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CoursePageRepository extends JpaRepository<CoursePage, Long> {
    CoursePage findCoursePageByCourseId(Long courseId);
}
