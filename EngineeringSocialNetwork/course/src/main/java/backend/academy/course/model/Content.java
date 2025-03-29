package backend.academy.course.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.Data;

@SuppressWarnings("MissingJavadocType")
@Entity
@Data
public class Content {
    @Id
    @GeneratedValue
    private Long id;
    private Long courseId;
    private String contentType;
    private String contentUrl;
}
