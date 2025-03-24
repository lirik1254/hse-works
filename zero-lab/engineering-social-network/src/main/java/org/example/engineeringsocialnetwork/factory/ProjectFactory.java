package org.example.engineeringsocialnetwork.factory;

import java.util.ArrayList;
import lombok.Getter;
import org.example.engineeringsocialnetwork.entities.Project;



public class ProjectFactory {
    @Getter
    private ArrayList<Project> projects = new ArrayList<>();

    public ProjectFactory() {
        fill();
    }

    public void fill() {
        Project project = new Project("Крутой проект", "Крутое описание");
        Project project1 = new Project("Крутой проект1", "Крутое описание1");
        Project project2 = new Project("Крутой проект2", "Крутое описание2");

        projects.add(project);
        projects.add(project1);
        projects.add(project2);
    }
}
