package backend.academy.user.dto;

import lombok.Data;

@Data
public class CreateUserCommand {
    private String name;
    private String email;
}
