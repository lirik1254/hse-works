package backend.academy.course.dto;

import lombok.Data;

@Data
public class CreateModuleCommand {
    private Long courseId;
    private String name;
    private String description;
}
