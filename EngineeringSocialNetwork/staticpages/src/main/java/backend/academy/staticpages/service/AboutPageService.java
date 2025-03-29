package backend.academy.staticpages.service;

import backend.academy.staticpages.entity.AboutPage;
import backend.academy.staticpages.repository.AboutPageRepository;
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
@SuppressWarnings("MagicNumber")
public class AboutPageService {
    private static final String ABOUT_PAGES_CACHE_KEY = "aboutPagesCache";
    private static final String ABOUT_PAGE_CACHE_KEY = "aboutPageCache";
    private final AboutPageRepository aboutPageRepository;
    private final RedisTemplate<String, Object> redisTemplate;
    ValueOperations<String, Object> valueOps;

    @PostConstruct
    public void valueOpsInit() {
        valueOps = redisTemplate.opsForValue();
    }

    @Transactional
    @Async
    public CompletableFuture<AboutPage> getPageByUserId(Long userId) {
        String key = ABOUT_PAGE_CACHE_KEY + userId;
        AboutPage aboutPage = (AboutPage) valueOps.get(key);

        if (aboutPage != null) {
            log.info("get about page from redis");
            return CompletableFuture.completedFuture(aboutPage);
        }
        log.info("get about page from DB");
        aboutPage = aboutPageRepository.findAboutPageByUserId(userId);
        valueOps.set(key, aboutPage);
        return CompletableFuture.completedFuture(aboutPage);
    }

    @Transactional
    @Async
    public void createPageByUserId(Long userId, String content) throws ExecutionException, InterruptedException {
        if (getAllPages().get().stream()
                .filter(s -> s.getUserId().equals(userId))
                .toList()
                .isEmpty()) {
            AboutPage aboutPage = new AboutPage();
            aboutPage.setContent(content);
            aboutPage.setUserId(userId);

            aboutPageRepository.save(aboutPage);
        } else {
            AboutPage pageByUserId = getPageByUserId(userId).get();
            pageByUserId.setContent(content);
            aboutPageRepository.save(pageByUserId);
        }
    }

    @Transactional
    @Async
    public CompletableFuture<List<AboutPage>> getAllPages() {
        List<AboutPage> cachedPages = (List<AboutPage>) valueOps.get(ABOUT_PAGES_CACHE_KEY);

        if (cachedPages != null) {
            log.info("get all pages from redis");
            return CompletableFuture.completedFuture(cachedPages);
        }
        log.info("get all pages from DB");
        List<AboutPage> aboutPages = aboutPageRepository.findAll();
        valueOps.set(ABOUT_PAGES_CACHE_KEY, aboutPages, 10, TimeUnit.SECONDS);

        return CompletableFuture.completedFuture(aboutPages);
    }
}
