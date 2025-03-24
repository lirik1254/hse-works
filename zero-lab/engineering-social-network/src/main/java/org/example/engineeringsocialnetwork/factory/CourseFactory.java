package org.example.engineeringsocialnetwork.factory;

import java.time.LocalDate;
import java.util.ArrayList;
import lombok.Getter;
import org.example.engineeringsocialnetwork.entities.Course;



@Getter
@SuppressWarnings("MagicNumber")
public class CourseFactory {
    private ArrayList<Course> courses = new ArrayList<>();

    public CourseFactory() {
        fill();
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
