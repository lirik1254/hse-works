package backend.academy.staticpages.controller;

import backend.academy.staticpages.entity.AboutPage;
import backend.academy.staticpages.service.AboutPageService;
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
@RequestMapping("/about-pages")
@RequiredArgsConstructor
public class AboutPageController {
    private final AboutPageService aboutPageService;

    @GetMapping
    public List<AboutPage> getPages() throws ExecutionException, InterruptedException {
        return aboutPageService.getAllPages().get();
    }

    @GetMapping("/{userId}")
    public AboutPage getPageByUserId(@PathVariable Long userId) throws ExecutionException, InterruptedException {
        return aboutPageService.getPageByUserId(userId).get();
    }

    @PostMapping("/{userId}")
    public void createPage(@PathVariable Long userId, @RequestBody String content)
            throws ExecutionException, InterruptedException {
        aboutPageService.createPageByUserId(userId, content);
    }
}
