package org.example.engineeringsocialnetwork.service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import lombok.Getter;
import org.example.engineeringsocialnetwork.entities.Course;


@SuppressWarnings("MagicNumber")
@Getter
public class CourseService {
    private final List<Course> courses = new ArrayList<>();

    public CourseService() {
        fill();
    }

    public void addCourse(String title, String group, LocalDate start, LocalDate end) {
        courses.add(new Course(title, group, start, end));
    }

    public void updateCourseTitle(String oldTitle, String newTitle) {
        for (Course course : courses) {
            if (course.getCourseTitle().equals(oldTitle)) {
                course.setCourseTitle(newTitle);
            }
        }
    }

    public void deleteCourse(String title) {
        courses.removeIf(course -> course.getCourseTitle().equals(title));
    }


    private void fill() {
        Course course = new Course("Инженерная дисциплина1", "PI-21-2",
                LocalDate.of(2025, 1, 17), LocalDate.of(2025, 2, 28));
        Course course1 = new Course("Инженерная дисциплина2", "PI-20-2",
                LocalDate.of(2025, 3, 10), LocalDate.of(2025, 5, 15));
        Course course2 = new Course("Инженерная дисциплина3", "PI-18-20",
                LocalDate.of(2025, 5, 10), LocalDate.of(2025, 7, 15));

        courses.add(course);
        courses.add(course1);
        courses.add(course2);
    }
}
