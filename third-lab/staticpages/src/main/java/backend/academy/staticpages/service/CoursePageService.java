package backend.academy.staticpages.service;

import backend.academy.staticpages.entity.CoursePage;
import backend.academy.staticpages.repository.CoursePageRepository;
import jakarta.annotation.PostConstruct;
import jakarta.transaction.Transactional;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;



@Service
@RequiredArgsConstructor
@Slf4j
public class CoursePageService {
    private static final String STATIC_COURSE_PAGES_KEY = "coursePagesCache";
    private static final String STATIC_COURSE_PAGE_KEY = "coursePageCache";
    private final CoursePageRepository coursePageRepository;
    private final RedisTemplate<String, Object> redisTemplate;
    ValueOperations<String, Object> valueOps;
    private static final int TIME_TO_LIVE = 10;

    @PostConstruct
    public void setValueOps() {
        valueOps = redisTemplate.opsForValue();
    }

    @Async
    @Transactional
    public CompletableFuture<CoursePage> getCoursePageByCourseId(Long courseId) {
        String key = STATIC_COURSE_PAGE_KEY + courseId;
        CoursePage coursePage = (CoursePage) valueOps.get(key);
        if (coursePage != null) {
            log.info("get course page from redis");
            return CompletableFuture.completedFuture(coursePage);
        }
        log.info("get course page from DB");
        coursePage = coursePageRepository.findCoursePageByCourseId(courseId);
        valueOps.set(key, coursePage, TIME_TO_LIVE, TimeUnit.SECONDS);
        return CompletableFuture.completedFuture(coursePage);
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
        List<CoursePage> coursePages = (List<CoursePage>) valueOps.get(STATIC_COURSE_PAGES_KEY);

        if (coursePages != null) {
            log.info("get course pages from redis");
            return CompletableFuture.completedFuture(coursePages);
        }
        log.info("get course pages from DB");
        List<CoursePage> aboutPages = coursePageRepository.findAll();
        valueOps.set(STATIC_COURSE_PAGE_KEY, aboutPages, TIME_TO_LIVE, TimeUnit.SECONDS);

        return CompletableFuture.completedFuture(aboutPages);
    }
}
