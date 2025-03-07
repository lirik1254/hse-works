package backend.academy.staticpages.service;

import backend.academy.staticpages.entity.AboutPage;
import backend.academy.staticpages.repository.AboutPageRepository;
import jakarta.transaction.Transactional;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;



@Service
@RequiredArgsConstructor
public class AboutPageService {
    private final AboutPageRepository aboutPageRepository;

    @Transactional
    @Async
    public CompletableFuture<AboutPage> getPageByUserId(Long userId) {
        return CompletableFuture.completedFuture(aboutPageRepository.findAboutPageByUserId(userId));
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
        return CompletableFuture.completedFuture(aboutPageRepository.findAll());
    }
}
