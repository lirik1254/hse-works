package org.example.laba.models;


import jakarta.persistence.*;
import org.example.laba.models.composite.DocumentCommentId;

@Entity
public class DocumentComment {

    @EmbeddedId
    private DocumentCommentId id;

    @ManyToOne
    @MapsId("documentId")
    @JoinColumn(name = "document_id")
    private Document document;

    @ManyToOne
    @MapsId("commentId")
    @JoinColumn(name = "comment_id")
    private Comment comment;

    // Getters and setters
}