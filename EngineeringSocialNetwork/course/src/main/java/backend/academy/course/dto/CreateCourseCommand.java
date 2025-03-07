package backend.academy.course.dto;

import lombok.Data;

@Data
public class CreateCourseCommand {
    private String name;
    private String description;
}
