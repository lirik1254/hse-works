## Диаграмма контейнеров
![Диаграмма контейнеров](https://github.com/user-attachments/assets/85cdb96e-af40-47af-a5e0-4c8071543866)\

## Взял этот компонент
![Компонент](https://github.com/user-attachments/assets/40a6b46d-0719-47cb-80af-520ca178d0ab)

## Составил для него схему БД
![Схема БД](https://github.com/user-attachments/assets/9600f50f-0a26-4598-820b-6c3f6cd0a621)

## Реализовал api (см. в LabWork №4/docs/api)

## Документация

### 1.1 GET /users 
**Метод**: GET  
**Описание**: Получить список всех пользователей.  
**Запрос**:  
• Нет параметров запроса.  
**Ответ**:  
• Код ответа: 200 OK  
• Тело ответа: JSON-массив всех пользователей.  
**Пример ответа**:
```json
[
    {
        "userId": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "ADMIN",
        "profilePicture": "url_to_picture"
    },
    {
        "userId": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "role": "USER",
        "profilePicture": "url_to_picture"
    }
]
```

### 1.2 GET /users/{id}
**Метод**: GET  
**Описание**: Получить информацию о пользователе по его ID.  
**Запрос**:  
• Параметры URL: `{id}` — ID пользователя, которого нужно получить.  
**Ответ**:  
• Код ответа: 200 OK / 404 Not Found (если не найден)  
• Тело ответа: JSON-объект пользователя / Сообщение об ошибке  
**Пример ответа**:
```json
{
    "userId": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "ADMIN",
    "profilePicture": "url_to_picture"
}
```
User not found with id: 5

## 1.3 POST /users

**Метод:** POST  
**Описание:** Создать нового пользователя.
### Запрос:
- **Тело запроса:** JSON-объект, содержащий данные пользователя.
**Пример тела запроса:**
```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123",
    "role": "USER",
    "profilePicture": "url_to_picture"
}
```
### Ответ:
- **Код ответа:**
  - 201 Created
  - 400 Bad Request (если неправильно заполнено тело запроса)
  - 500 Internal Server Error (если неправильное тело запроса)

- **Тело ответа:**
  - JSON-объект созданного пользователя
  - Строка ошибки (в случае ошибки)

**Пример ответа:**
```json
{
    "userId": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "USER",
    "profilePicture": "url_to_picture"
}
```
Не удалось создать пользователя

### 1.4 PUT /users/{id}
**Метод:** PUT  
**Описание:** Обновить информацию о пользователе.  
**Запрос:**
- Параметры URL: `{id}` — ID пользователя, которого нужно обновить.
- Тело запроса: JSON-объект с данными для обновления.

**Пример тела запроса:**
```json
{
    "name": "John Doe Updated",
    "email": "john.doe.updated@example.com",
    "password": "newpassword123",
    "role": "ADMIN",
    "profilePicture": "new_url_to_picture"
}
```
**Ответ:**

- **Код ответа:**
  - 200 OK
  - 404 Not Found (если пользователь не найден)
  - 500 Internal Server Error (если неверное тело запроса)

- **Тело ответа:** JSON-объект обновленного пользователя / Строка ошибки

**Пример ответа:**
```json
{
    "userId": 1,
    "name": "John Doe Updated",
    "email": "john.doe.updated@example.com",
    "role": "ADMIN",
    "profilePicture": "new_url_to_picture"
}
```
User not found with id: 15

Internal server error: Required request body is missing: public org.springframework.http.ResponseEntity<org.example.laba.models.User> org.example.laba.controllers.UserController.updateUser(java.lang.Integer,org.example.laba.models.User)

**1.5 DELETE /users/{id}**

- **Метод:** DELETE
- **Описание:** Удалить пользователя по его ID.

**Запрос:**
- Параметры URL: `{id}` — ID пользователя, которого нужно удалить.

**Ответ:**
- **Код ответа:**
  - 200 OK
  - 404 Not Found (если пользователь не найден)

**Пример ответа:**
```json
{
    "message": "User deleted successfully."
}
```
User not found with id: 5


**2.1 GET /posts**

- **Метод:** GET
- **Описание:** получить список всех постов.

**Запрос:**
- Нет параметров запроса.

**Ответ:**
- **Код ответа:** 200 OK
- **Тело ответа:** JSON-массив всех постов.

**Пример ответа:**
```json
[
    {
        "postId": 1,
        "title": "Post 1",
        "postText": "This is the first post.",
        "photosUrlFolder": "url_to_photos_folder",
        "uploadDate": "2025-01-18T14:30:00",
        "author": {
            "userId": 1,
            "name": "John Doe"
        }
    },
    {
        "postId": 2,
        "title": "Post 2",
        "postText": "This is the second post.",
        "photosUrlFolder": "url_to_photos_folder",
        "uploadDate": "2025-01-18T14:45:00",
        "author": {
            "userId": 1,
            "name": "John Doe",
            "email": "Alo",
            "password": "GoAway",
            "role": "bestie",
            "profilePicture": "alice.jpg"
        }
    }
]
```

**2.2 GET /posts/{id}**

- **Метод:** GET
- **Описание:** Получить информацию о посте по его ID.

**Запрос:**
- **Параметры URL:** {id} — ID поста, который нужно получить.

**Ответ:**
- **Код ответа:** 200 OK, 404 Not Found (если не существует такого поста)
- **Тело ответа:** JSON-объект поста / Сообщение об ошибке.

**Пример ответа:**
```json
{
    "postId": 1,
    "title": "Post 1",
    "postText": "This is the first post.",
    "photosUrlFolder": "url_to_photos_folder",
    "uploadDate": "2025-01-18T14:30:00",
    "author": {
        "userId": 1,
        "name": "John Doe",
        "email": "Alo",
        "password": "GoAway",
        "role": "bestie",
        "profilePicture": "alice.jpg"
    }
}
```
Post not found with id: 5


**2.3 POST /posts**

- **Метод:** POST
- **Описание:** Создать новый пост.

**Запрос:**
- **Тело запроса:** JSON-объект, содержащий данные поста.

**Пример запроса:**
```json
{
    "title": "New Post",
    "postText": "This is a new post.",
    "photosUrlFolder": "url_to_photos_folder",
    "uploadDate": "2025-01-18T15:00:00",
    "authorId": 1
}
```
**Ответ:**

- **Код ответа:** 
  - 201 Created
  - 400 (если неправильное тело запроса)
  - 500 Internal Server Error (если некорректный запрос)

- **Тело ответа:** JSON-объект созданного поста.

**Пример ответа:**
```json
{
    "postId": 3,
    "title": "New Post",
    "postText": "This is a new post.",
    "photosUrlFolder": "url_to_photos_folder",
    "uploadDate": "2025-01-18T15:00:00",
    "author": {
        "userId": 1,
        "name": "John Doe",
        "email": "Alo",
        "password": "GoAway",
        "role": "bestie",
        "profilePicture": "alice.jpg"
    }
}
```
Internal server error: Required request body is missing: public org.springframework.http.ResponseEntity<org.example.laba.models.Post> org.example.laba.controllers.PostController.createPost(org.example.laba.models.Post)
Не удалось создать пост

**2.4 PUT /posts/{id}**

**Метод:** PUT  
**Описание:** Обновить информацию о посте.

### Запрос:
- **Параметры URL:** {id} — ID поста, который нужно обновить.
- **Тело запроса:** JSON-объект с данными для обновления.

**Пример запроса:**
```json
{
    "title": "Updated Post",
    "postText": "This is an updated post.",
    "photosUrlFolder": "updated_url_to_photos_folder",
    "uploadDate": "2025-01-18T16:00:00",
    "authorId": 1
}
```
**Код ответа:**
- 200 OK
- 404 (если не найден пост)
- 500 Internal Server Error (если неправильный ввод тела запроса)

**Тело ответа:** JSON-объект обновленного поста или сообщение об ошибке.

### Пример ответа:
```json
{
    "postId": 3,
    "title": "Updated Post",
    "postText": "This is an updated post.",
    "photosUrlFolder": "updated_url_to_photos_folder",
    "uploadDate": "2025-01-18T16:00:00",
    "author": {
        "userId": 1,
        "name": "John Doe",
        "email": "Alo",
        "password": "GoAway",
        "role": "bestie",
        "profilePicture": "alice.jpg"
    }
}
```
Internal server error: Required request body is missing: public org.springframework.http.ResponseEntity<org.example.laba.models.Post> org.example.laba.controllers.PostController.updatePost(java.lang.Integer,org.example.laba.models.Post)
Post not found with id: 52

## 2.5 DELETE /posts/{id}

**Метод:** DELETE  
**Описание:** Удалить пост по его ID.  

**Запрос:**
- Параметры URL: `{id}` — ID поста, который нужно удалить.

**Ответ:**
- Код ответа: 200 OK или 404 Not Found (если пост не найден)
- Строка с сообщением об успехе или ошибке.

### Пример ответа:
```txt
Post deleted successfully.
```
Post not found with id: 5

## 3.1 GET /documents

**Метод:** GET  
**Описание:** Получить список всех документов.

**Запрос:**
- Нет параметров запроса.

**Ответ:**
- Код ответа: 200 OK
- Тело ответа: JSON-массив всех документов.

### Пример ответа:
```json
[
    {
        "documentId": 1,
        "title": "Document 1",
        "fileUrl": "url_to_document",
        "category": "Technical",
        "uploadDate": "2025-01-18T14:30:00",
        "author": {
            "userId": 1,
            "name": "John Doe",
            "email": "Alo",
            "password": "GoAway",
            "role": "bestie",
            "profilePicture": "alice.jpg"
        }
    }
]
```

## 3.2 GET /documents/{id}

**Метод:** GET  
**Описание:** Получить информацию о документе по его ID.

**Запрос:**
- Параметры URL: `{id}` — ID документа, который нужно получить.

**Ответ:**
- Код ответа: 200 OK, 404 Not Found если нет документа с таким id.
- Тело ответа: JSON-объект документа или сообщение об ошибке.

### Пример ответа:
```json
{
    "documentId": 1,
    "title": "Document 1",
    "fileUrl": "url_to_document",
    "category": "Technical",
    "uploadDate": "2025-01-18T14:30:00",
    "author": {
        "userId": 1,
        "name": "John Doe",
        "email": "Alo",
        "password": "GoAway",
        "role": "bestie",
        "profilePicture": "alice.jpg"
    }
}
```
Document not found with id: 5

## 3.3 POST /documents

**Метод:** POST  
**Описание:** Создать новый документ.

**Запрос:**
- Тело запроса: JSON-объект, содержащий данные документа.

### Пример запроса:
```json
{
    "title": "New Document",
    "fileUrl": "url_to_document",
    "category": "Research",
    "uploadDate": "2025-01-18T15:00:00",
    "authorId": 1
}
```
## Ответ:

**Код ответа:** 
- 201 Created
- 400 если неправильное тело запроса
- 500 Internal Server Error если некорректный запрос.

**Тело ответа:** JSON-объект созданного документа или текст ошибки.

### Пример ответа:
```json
{
    "documentId": 2,
    "title": "New Document",
    "fileUrl": "url_to_document",
    "category": "Research",
    "uploadDate": "2025-01-18T15:00:00",
    "author": {
        "userId": 1,
        "name": "John Doe",
        "email": "Alo",
        "password": "GoAway",
        "role": "bestie",
        "profilePicture": "alice.jpg"
    }
}
```
Internal server error: Required request body is missing: public org.springframework.http.ResponseEntity<org.example.laba.models.Document> org.example.laba.controllers.DocumentController.createDocument(org.example.laba.models.Document)

## 3.4 PUT /documents/{id}

**Метод:** PUT  
**Описание:** Обновить информацию о документе.

### Запрос:
- **Параметры URL:** {id} — ID документа, который нужно обновить.
- **Тело запроса:** JSON-объект с данными для обновления.

### Пример запроса:
```json
{
    "title": "Updated Document",
    "fileUrl": "updated_url_to_document",
    "category": "Updated Research",
    "uploadDate": "2025-01-18T16:00:00",
    "authorId": 1
}
```
### Ответ:
- **Код ответа:** 200 OK, 404, 500 Internal Server Error если неправильное тело запроса.
- **Тело ответа:** JSON-объект обновленного документа / Текст ошибки.

### Пример ответа:
```json
{
    "documentId": 2,
    "title": "Updated Document",
    "fileUrl": "updated_url_to_document",
    "category": "Updated Research",
    "uploadDate": "2025-01-18T16:00:00",
    "author": {
        "userId": 1,
        "name": "John Doe",
        "email": "Alo",
        "password": "GoAway",
        "role": "bestie",
        "profilePicture": "alice.jpg"
    }
}
```
Internal server error: Required request body is missing: public org.springframework.http.ResponseEntity<org.example.laba.models.Document> org.example.laba.controllers.DocumentController.updateDocument(java.lang.Integer,org.example.laba.models.Document)
Document not found with id: 15

### 3.5 DELETE /documents/{id}

**Метод:** DELETE  
**Описание:** Удалить документ по его ID.  

#### Запрос:
- Параметры URL: `{id}` — ID документа, который нужно удалить.

#### Ответ:
- **Код ответа:** 200 OK или 404 Not Found, если документ не найден.

#### Пример ответа:
Document deleted successfully.
Document not found with id: 5


## Тестирование API

### 1.1 GET /users
![image](https://github.com/user-attachments/assets/821594a6-0ce3-4a1f-8dff-630fd954c4bb)
![image](https://github.com/user-attachments/assets/91e86c71-7a98-46d1-86e6-d28ee980bd33)
### 1.2 GET /users/{id}
![image](https://github.com/user-attachments/assets/335b47ff-8cd9-4924-9a89-967316eb55eb)
### 1.3  POST /users
![image](https://github.com/user-attachments/assets/3b9e189d-5fd8-4675-a33d-aa656c9eb8e9)
![image](https://github.com/user-attachments/assets/188ed320-9000-4571-a715-2b783f002bb6)
### 1.4 PUT /users/{id}
![image](https://github.com/user-attachments/assets/e9e8c8a6-5a47-474c-9eab-f0889892458e)
![image](https://github.com/user-attachments/assets/2f815180-b769-4125-a9f5-3f6510abcf7d)
### 1.5 DELETE /users/{id}
![image](https://github.com/user-attachments/assets/3df062e6-b979-4a16-b5fd-38b62758b5fc)
![image](https://github.com/user-attachments/assets/ca156fa0-127c-47d7-8349-daaba9c3e9d3)

### 2.1 GET /posts 
![image](https://github.com/user-attachments/assets/ad60a8bf-8478-44b3-af3a-b49f6a40058a)
![image](https://github.com/user-attachments/assets/33516953-58ba-41c8-98d4-93c8cb0e4b3e)
### 2.2 GET /posts/{id}
![image](https://github.com/user-attachments/assets/82546c89-1a94-4bc2-9694-910c8df95d05)
![image](https://github.com/user-attachments/assets/17b97a6a-a0e0-4228-8e59-0ad24b08f744)
### 2.3 POST /posts
![image](https://github.com/user-attachments/assets/4dec451b-f2bd-4a5b-b9df-97b6a56e08bb)
![image](https://github.com/user-attachments/assets/331a1ebc-b207-4d31-bb69-30ea6a6f29b7)
### 2.4 PUT /posts/{id}
![image](https://github.com/user-attachments/assets/7087f2f9-6954-4043-ad26-cc110dd8fbd6)
![image](https://github.com/user-attachments/assets/66d75738-f56f-48be-b8bc-2449018161d2)
### 2.5 DELETE /posts/{id}
![image](https://github.com/user-attachments/assets/24946974-088b-4926-a607-c9a03d7ef4dd)
![image](https://github.com/user-attachments/assets/d2565aff-1ac3-426f-9513-f25522dfb04b)

### 3.1 GET /documents
![image](https://github.com/user-attachments/assets/a9ea1aef-fe67-4f1a-88e7-6dda41f39cbf)
![image](https://github.com/user-attachments/assets/6e55d3fd-dc68-40e1-9f28-11b260fbefb5)
### 3.2 GET /documents/{id}
![image](https://github.com/user-attachments/assets/ac4f3e20-34ec-403e-b0df-7ee849914113)
![image](https://github.com/user-attachments/assets/0e9273d1-ddaf-4407-849d-458f4f6c8767)
### 3.3 POST /documents
![image](https://github.com/user-attachments/assets/daf3ec3f-9193-440f-93d7-3513fd9cae8a)
![image](https://github.com/user-attachments/assets/d68991a1-52c6-4866-9217-85049a246fc0)
### 3.4 PUT /documents/{id}
![image](https://github.com/user-attachments/assets/04978528-7479-451b-b18e-bea5a532ba15)
![image](https://github.com/user-attachments/assets/68aef5f8-c2ac-4b20-9d92-3af3b2d1dab7)
### 3.5 DELETE /documents/{id}
![image](https://github.com/user-attachments/assets/569c3787-5e73-4df7-a88d-8d329284f6ea)
![image](https://github.com/user-attachments/assets/49a81d82-cb20-4f0b-8acc-a338b66f544d)











