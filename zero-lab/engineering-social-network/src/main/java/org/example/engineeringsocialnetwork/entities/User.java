package org.example.engineeringsocialnetwork.entities;

import java.time.LocalDate;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;



@Getter
@Setter
@AllArgsConstructor
@ToString
public class User {
    private int age;
    private String role;
    private String city;
    private String status;
    private LocalDate registeredAt;
}
