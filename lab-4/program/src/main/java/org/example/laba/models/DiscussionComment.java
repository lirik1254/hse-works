package org.example.laba.models;

import jakarta.persistence.*;
import org.example.laba.models.composite.DiscussionCommentId;

@Entity
public class DiscussionComment {

    @EmbeddedId
    private DiscussionCommentId id;

    @ManyToOne
    @MapsId("discussionId")
    @JoinColumn(name = "discussion_id")
    private Discussion discussion;

    @ManyToOne
    @MapsId("commentId")
    @JoinColumn(name = "comment_id")
    private Comment comment;

    // Getters and setters
}
