package org.example.laba.models;

import jakarta.persistence.*;
import org.example.laba.models.composite.PostCommentId;

@Entity
public class PostComment {

    @EmbeddedId
    private PostCommentId id;

    @ManyToOne
    @MapsId("postId")
    @JoinColumn(name = "post_id")
    private Post post;

    @ManyToOne
    @MapsId("commentId")
    @JoinColumn(name = "comment_id")
    private Comment comment;

    // Getters and setters
}
