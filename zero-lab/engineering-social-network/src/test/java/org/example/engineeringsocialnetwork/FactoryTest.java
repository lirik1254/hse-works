package org.example.engineeringsocialnetwork;

import org.example.engineeringsocialnetwork.factory.ProjectFactory;
import org.example.engineeringsocialnetwork.factory.UserFactory;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class FactoryTest {
    @Test
    public void ProjectFactoryTest() {
        ProjectFactory projectFactory = new ProjectFactory();
        assertEquals(3, projectFactory.getProjects().size());
    }

    @Test
    public void UserFactoryTest() {
        UserFactory userFactory = new UserFactory();
        assertEquals(3, userFactory.getUsers().size());
    }
}
