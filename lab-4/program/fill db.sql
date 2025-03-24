-- Создание таблицы user
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    profile_picture VARCHAR
);

-- Создание таблицы document
CREATE TABLE document (
    document_id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    file_url VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    upload_date TIMESTAMP NOT NULL,
    author_id INTEGER NOT NULL REFERENCES "user" (user_id)
);

-- Создание таблицы post
CREATE TABLE post (
    post_id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    photos_url_folder VARCHAR NOT NULL,
    post_text VARCHAR NOT NULL,
    upload_date TIMESTAMP NOT NULL,
    author_id INTEGER NOT NULL REFERENCES "user" (user_id)
);

-- Создание таблицы discussion
CREATE TABLE discussion (
    discussion_id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    author_id INTEGER NOT NULL REFERENCES "user" (user_id)
);

-- Создание таблицы comment
CREATE TABLE comment (
    comment_id SERIAL PRIMARY KEY,
    comment_text VARCHAR NOT NULL,
    author_id INTEGER NOT NULL REFERENCES "user" (user_id)
);

-- Создание таблицы discussion_comment
CREATE TABLE discussion_comment (
    discussion_id INTEGER NOT NULL REFERENCES discussion (discussion_id),
    comment_id INTEGER NOT NULL REFERENCES comment (comment_id),
    PRIMARY KEY (discussion_id, comment_id)
);

-- Создание таблицы post_comment
CREATE TABLE post_comment (
    post_id INTEGER NOT NULL REFERENCES post (post_id),
    comment_id INTEGER NOT NULL REFERENCES comment (comment_id),
    PRIMARY KEY (post_id, comment_id)
);

-- Создание таблицы document_comment
CREATE TABLE document_comment (
    document_id INTEGER NOT NULL REFERENCES document (document_id),
    comment_id INTEGER NOT NULL REFERENCES comment (comment_id),
    PRIMARY KEY (document_id, comment_id)
);

-- Вставка тестовых данных в таблицу user
INSERT INTO "user" (name, email, password, role, profile_picture) VALUES
('Alice', 'alice@example.com', 'password123', 'admin', 'alice.jpg'),
('Bob', 'bob@example.com', 'password123', 'user', 'bob.jpg'),
('Charlie', 'charlie@example.com', 'password123', 'moderator', 'charlie.jpg');

-- Вставка тестовых данных в таблицу document
INSERT INTO document (title, file_url, category, upload_date, author_id) VALUES
('Document 1', '/files/doc1.pdf', 'Engineering', NOW(), 1),
('Document 2', '/files/doc2.pdf', 'Science', NOW(), 2);

-- Вставка тестовых данных в таблицу post
INSERT INTO post (title, photos_url_folder, post_text, upload_date, author_id) VALUES
('Post 1', '/photos/post1/', 'This is the first post.', NOW(), 1),
('Post 2', '/photos/post2/', 'This is the second post.', NOW(), 3);

-- Вставка тестовых данных в таблицу discussion
INSERT INTO discussion (title, description, author_id) VALUES
('Discussion 1', 'Discussion about engineering.', 1),
('Discussion 2', 'Discussion about science.', 2);

-- Вставка тестовых данных в таблицу comment
INSERT INTO comment (comment_text, author_id) VALUES
('Great post!', 2),
('Interesting topic.', 3),
('Thanks for sharing!', 1);

-- Вставка тестовых данных в таблицу discussion_comment
INSERT INTO discussion_comment (discussion_id, comment_id) VALUES
(1, 1),
(2, 2);

-- Вставка тестовых данных в таблицу post_comment
INSERT INTO post_comment (post_id, comment_id) VALUES
(1, 3),
(2, 2);

-- Вставка тестовых данных в таблицу document_comment
INSERT INTO document_comment (document_id, comment_id) VALUES
(1, 1),
(2, 3);
