package org.example.engineeringsocialnetwork;
import org.example.engineeringsocialnetwork.service.CourseService;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

public class CourseServiceTest {
    @Test
    public void courseServiceCreateTest() {
        CourseService courseService = new CourseService();
        assertEquals(3, courseService.getCourses().size());
    }

    @Test
    public void addCourseServiceTest() {
        CourseService courseService = new CourseService();

        courseService.addCourse("Курс", "ПИ-21-2", LocalDate.of(2020, 10, 10), LocalDate.of(2010, 12, 12));
        assertEquals(4, courseService.getCourses().size());
    }

    @Test
    public void updateCourseServiceTest() {
        CourseService courseService = new CourseService();

        assertTrue(courseService
                .getCourses()
                .stream()
                .anyMatch(s -> s.getCourseTitle().equals("Инженерная дисциплина1")));

        assertTrue(courseService.getCourses()
                .stream()
                .noneMatch(s -> s.getCourseTitle().equals("Лол")));

        courseService.updateCourseTitle("Инженерная дисциплина1", "Лол");

        assertTrue(courseService.getCourses()
                .stream()
                .noneMatch(s -> s.getCourseTitle().equals("Инженерная дисциплина1")));

        assertTrue(courseService.getCourses()
                .stream()
                .anyMatch(s -> s.getCourseTitle().equals("Лол")));
    }

    @Test
    public void deleteCourseServiceTest() {
        CourseService courseService = new CourseService();

        assertEquals(3, courseService.getCourses().size());

        courseService.deleteCourse("Инженерная дисциплина1");

        assertEquals(2, courseService.getCourses().size());
    }

}
