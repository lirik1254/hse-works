package backend.academy.staticpages.controller;

import backend.academy.staticpages.entity.CoursePage;
import backend.academy.staticpages.service.CoursePageService;
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
@RequestMapping("/course-pages")
@RequiredArgsConstructor
public class CoursePageController {
    private final CoursePageService coursePageService;

    @GetMapping
    public List<CoursePage> getPages() throws ExecutionException, InterruptedException {
        return coursePageService.getAllCoursePages().get();
    }

    @GetMapping("/{courseId}")
    public CoursePage getPage(@PathVariable Long courseId)
            throws ExecutionException, InterruptedException {
        return coursePageService.getCoursePageByCourseId(courseId).get();
    }

    @PostMapping("/{courseId}")
    public void createPage(@PathVariable Long courseId, @RequestBody String content)
            throws ExecutionException, InterruptedException {
        coursePageService.createPageByCourseId(courseId, content);
    }

}
