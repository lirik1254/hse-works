package org.example.laba.controllers;

import org.example.laba.models.Post;
import org.example.laba.models.User;
import org.example.laba.services.PostService;
import org.example.laba.services.UserService;
import org.example.laba.utils.exceptions.PostNotFoundException;
import org.example.laba.utils.exceptions.UserNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class PostController {

    private final PostService postService;
    private final UserService userService;

    @Autowired
    public PostController(PostService postService, UserService userService) {
        this.postService = postService;
        this.userService = userService;
    }

    @GetMapping("/posts")
    public List<Post> getAllPosts() {
        return postService.getAllPosts();
    }

    @GetMapping("/posts/{id}")
    public Post getPostById(@PathVariable Integer id) {
        return postService.getPostById(id)
                .orElseThrow(() -> new PostNotFoundException("Post not found with id: " + id));
    }

    @PostMapping("posts")
    public ResponseEntity<Post> createPost(@RequestBody Post post) {
        if (post.getAuthorId() != null) {
            User author = userService.getUserById(post.getAuthorId())
                    .orElseThrow(() -> new UserNotFoundException("User not found with id: " + post.getAuthorId()));
            post.setAuthor(author); // Устанавливаем пользователя по id
        }
        Post createdPost = postService.createPost(post);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdPost);
    }

    @PutMapping("/posts/{id}")
    public ResponseEntity<Post> updatePost(@PathVariable Integer id, @RequestBody Post post) {
        Post updatedPost = postService.updatePost(id, post);
        return ResponseEntity.ok(updatedPost);
    }

    @DeleteMapping("/posts/{id}")
    public ResponseEntity<String> deletePost(@PathVariable Integer id) {
        try {
            postService.deletePost(id);
            return ResponseEntity.status(HttpStatus.OK).body("Post deleted successfully.");
        } catch (PostNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Post not found with id: " + id);
        }
    }
}
