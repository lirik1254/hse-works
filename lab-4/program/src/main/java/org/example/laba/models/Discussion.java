package org.example.laba.models;

import jakarta.persistence.*;

@Entity
public class Discussion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer discussionId;

    private String title;
    private String description;

    @ManyToOne
    @JoinColumn(name = "author_id", referencedColumnName = "user_id")
    private User author; // Связь ManyToOne с User

    // геттеры и сеттеры
}
