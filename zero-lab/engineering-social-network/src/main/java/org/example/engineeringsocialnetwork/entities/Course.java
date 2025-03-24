package org.example.engineeringsocialnetwork.entities;

import java.time.LocalDate;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;



@AllArgsConstructor
@Getter
@Setter
@ToString
public class Course {
    private String courseTitle;
    private String groupName;
    private LocalDate startDate;
    private LocalDate endDate;
}
