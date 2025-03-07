package backend.academy.staticpages.service;

import backend.academy.staticpages.entity.CoursePage;
import backend.academy.staticpages.repository.CoursePageRepository;
import jakarta.transaction.Transactional;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CoursePageService {
    private final CoursePageRepository coursePageRepository;

    @Async
    @Transactional
    public CompletableFuture<CoursePage> getCoursePageByCourseId(Long courseId) {
        return CompletableFuture.completedFuture(coursePageRepository.findCoursePageByCourseId(courseId));
    }

    @Async
    @Transactional
    public void createPageByCourseId(Long courseId, String content) throws ExecutionException, InterruptedException {
        if (getAllCoursePages().get().stream()
                .filter(s -> s.getCourseId().equals(courseId))
                .toList()
                .isEmpty()) {
            CoursePage coursePage = new CoursePage();
            coursePage.setContent(content);
            coursePage.setCourseId(courseId);

            coursePageRepository.save(coursePage);
        } else {
            CoursePage pageByCourseId = getCoursePageByCourseId(courseId).get();
            pageByCourseId.setContent(content);
            coursePageRepository.save(pageByCourseId);
        }
    }

    @Async
    @Transactional
    public CompletableFuture<List<CoursePage>> getAllCoursePages() {
        return CompletableFuture.completedFuture(coursePageRepository.findAll());
    }
}
