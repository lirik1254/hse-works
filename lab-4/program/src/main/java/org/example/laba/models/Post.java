package org.example.laba.models;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
public class Post {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer postId;

    private String title;

    @Column(name = "photos_url_folder")
    private String photosUrlFolder;

    @Column(name = "post_text")
    private String postText;

    @Column(name = "upload_date")
    private LocalDateTime uploadDate;

    @ManyToOne
    @JoinColumn(name = "author_id", referencedColumnName = "user_id")
    private User author; // Связь ManyToOne с User

    @Transient
    private Integer authorId; // Временное поле для передачи только id

    // геттеры и сеттеры
}
