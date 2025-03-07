package backend.academy.course.controller;

import backend.academy.course.dto.CreateCourseCommand;
import backend.academy.course.dto.CreateModuleCommand;
import backend.academy.course.model.Course;
import backend.academy.course.model.Lesson;
import backend.academy.course.model.Module;
import backend.academy.course.service.CourseService;
import java.util.List;
import java.util.concurrent.ExecutionException;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/courses")
@RequiredArgsConstructor
public class CourseController {

    private final CourseService courseService;

    @PostMapping
    public Course createCourse(@RequestBody CreateCourseCommand command)
            throws ExecutionException, InterruptedException {
        return courseService.createCourse(command).get();
    }

    @PostMapping("/module")
    public Module createModule(@RequestBody CreateModuleCommand command)
            throws ExecutionException, InterruptedException {
        return courseService.createModule(command).get();
    }

    @PostMapping("/module/{moduleId}/lesson")
    public Lesson createLesson(@PathVariable Long moduleId, @RequestBody Lesson lesson)
            throws ExecutionException, InterruptedException {
        return courseService.createLesson(moduleId, lesson.getTitle(), lesson.getContent()).get();
    }

    @GetMapping
    public List<Course> getAllCourses() {
        return courseService.getAllCourses();
    }
}
