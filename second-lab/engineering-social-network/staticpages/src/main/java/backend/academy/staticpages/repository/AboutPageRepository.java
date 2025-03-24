package backend.academy.staticpages.repository;

import backend.academy.staticpages.entity.AboutPage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;

public interface AboutPageRepository extends JpaRepository<AboutPage, Long> {
    AboutPage findAboutPageByUserId(Long userId);

    @Modifying
    @Transactional
    @Query(value = "ALTER SEQUENCE about_page_id_seq RESTART WITH 1", nativeQuery = true)
    void resetSequence();
}
