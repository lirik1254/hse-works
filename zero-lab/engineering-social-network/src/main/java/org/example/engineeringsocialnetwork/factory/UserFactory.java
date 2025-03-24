package org.example.engineeringsocialnetwork.factory;

import java.time.LocalDate;
import java.util.ArrayList;
import lombok.Getter;
import org.example.engineeringsocialnetwork.entities.User;


@SuppressWarnings("MagicNumber")
public class UserFactory {
    @Getter
    private ArrayList<User> users = new ArrayList<>();

    public UserFactory() {
        fill();
    }

    public void fill() {
        User user = new User(18, "Преподаватель", "Пермь", "Я крутой препод",
                LocalDate.of(2020, 10, 10));
        User user1 = new User(20, "Ученик", "Москва", "Я лох ученик",
                LocalDate.of(2018, 10, 10));
        User user2 = new User(52, "Директор", "Нижневартовск", "Да здравствует",
                LocalDate.of(2000, 5, 2));

        users.add(user);
        users.add(user1);
        users.add(user2);
    }
}
