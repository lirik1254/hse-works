package org.example.laba.services;

import org.example.laba.models.Post;
import org.example.laba.repos.PostRepository;
import org.example.laba.utils.exceptions.PostCreationException;
import org.example.laba.utils.exceptions.PostNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class PostService {

    private final PostRepository postRepository;

    @Autowired
    public PostService(PostRepository postRepository) {
        this.postRepository = postRepository;
    }

    public List<Post> getAllPosts() {
        return postRepository.findAll();
    }

    public Post createPost(Post post) {
        try {
            return postRepository.save(post);
        } catch (Exception e) {
            throw new PostCreationException("Не удалось создать пост");
        }
    }

    public Optional<Post> getPostById(Integer id) {
        return postRepository.findById(id);
    }

    public Post updatePost(Integer id, Post post) {
        Post existingPost = postRepository.findById(id)
                .orElseThrow(() -> new PostNotFoundException("Post not found with id: " + id));

        if (post.getTitle() != null) {
            existingPost.setTitle(post.getTitle());
        }
        if (post.getPostText() != null) {
            existingPost.setPostText(post.getPostText());
        }
        if (post.getPhotosUrlFolder() != null) {
            existingPost.setPhotosUrlFolder(post.getPhotosUrlFolder());
        }

        try {
            return postRepository.save(existingPost);
        } catch (Exception e) {
            throw new RuntimeException("Error updating post", e);  // Обработка ошибки сохранения
        }
    }

    public void deletePost(Integer id) {
        if (!postRepository.existsById(id)) {
            throw new PostNotFoundException("Post not found with id: " + id);
        }
        postRepository.deleteById(id);
    }
}