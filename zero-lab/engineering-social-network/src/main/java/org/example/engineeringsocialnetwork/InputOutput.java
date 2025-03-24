package org.example.engineeringsocialnetwork;

import java.time.DateTimeException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;
import lombok.Getter;
import org.example.engineeringsocialnetwork.entities.Info;
import org.example.engineeringsocialnetwork.factory.ProjectFactory;
import org.example.engineeringsocialnetwork.factory.UserFactory;
import org.example.engineeringsocialnetwork.service.CourseService;


@SuppressWarnings({"RegexpSingleline", "RegexpSinglelineJava"})
public class InputOutput {

    public final String startDateString = "Введите дату начала курса в формате yyyy-mm-dd: ";

    @Getter
    private final String message = """
             Введите, что вы хотите сделать:
             0. Выход
             1. Вывести основную информацию
            
             2. Вывести список курсов
             3. Добавить курс
             4. Изменить заголовок курса
             5. Удалить курс
            
             6. Вывести список проектов
             7. Список людей
             8. Юридическая информация о компании           \s
            \s""";
    CourseService courseService = new CourseService();
    private Scanner in = new Scanner(System.in);

    private static void getUsers() {
        UserFactory userFactory = new UserFactory();
        userFactory.getUsers().forEach(System.out::println);
        System.out.println();
    }

    private static void getProjects() {
        ProjectFactory projectFactory = new ProjectFactory();
        projectFactory.getProjects().forEach(System.out::println);
        System.out.println();
    }

    public void setScanner(Scanner scanner) {
        in = scanner;
    }

    @SuppressWarnings("RegexpSinglelineJava")
    int getNumInput(int leftBorder, int rightBorder, String message) {

        System.out.print(message);

        int someIntValue;

        while (true) {
            if (in.hasNextInt()) {
                someIntValue = in.nextInt();
                in.nextLine();
                if (someIntValue < leftBorder || someIntValue > rightBorder) {
                    System.out.printf("Введенное число должно быть в диапазоне от %d до %d\n\n%s\n",
                            leftBorder, rightBorder, message);
                } else {
                    return someIntValue;
                }
            } else {
                in.nextLine();
                System.out.printf("Вы ввели не число!\n\n%s\n", message);
            }
        }
    }

    @SuppressWarnings({"MagicNumber", "MissingSwitchDefault", "RegexpSinglelineJava"})
    public void getStart() {
        int answer = getNumInput(0, 8, message);
        while (answer != 0) {
            switch (answer) {
                case 1 -> System.out.println(Info.MAIN_INFO);
                case 2 -> {
                    getCourses();
                }
                case 3 -> addCourse();
                case 4 -> editCourse();

                case 5 -> deleteCourse();

                case 6 -> {
                    getProjects();
                }
                case 7 -> {
                    getUsers();
                }
                case 8 -> System.out.println(Info.LEGAL_INFORMATION);
            }
            answer = getNumInput(0, 5, message);
        }
    }

    private void getCourses() {
        courseService.getCourses().forEach(System.out::println);
        System.out.println();
    }

    public LocalDate localDateInput(String message) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

        System.out.print(startDateString);
        String date = in.nextLine();
        while (true) {
            try {
                return LocalDate.parse(date, formatter);
            } catch (DateTimeException e) {
                System.out.print("Неверный ввод! Введите заново: ");
                date = in.nextLine();
            }
        }
    }

    public void addCourse() {
        System.out.print("Введите название курса: ");
        String title = in.nextLine();
        System.out.print("Введите название группы: ");
        String groupName = in.nextLine();
        LocalDate startDate = localDateInput(startDateString);
        LocalDate endDate = localDateInput("Введите дату окончания курса в формате yyyy-mm-dd: ");
        courseService.addCourse(title, groupName, startDate, endDate);
    }

    public void editCourse() {
        System.out.print("Введите старое название курса: ");
        String oldTitle = getTitle();
        System.out.print("Введите новое название курса: ");
        String newTitle = in.nextLine();

        courseService.updateCourseTitle(oldTitle, newTitle);
        System.out.println("Название курса успешно изменено!\n");
    }

    private String getTitle() {
        String title = in.nextLine();
        boolean isCorrect = false;

        while (!isCorrect) {
            String finalTitle = title;
            if (courseService.getCourses()
                    .stream()
                    .noneMatch(s -> s.getCourseTitle().equals(finalTitle))) {
                System.out.print("Вы ввели неверное название курса, введите заново: ");
                title = in.nextLine();
            } else {
                isCorrect = true;
            }
        }
        return title;
    }

    public void deleteCourse() {
        System.out.println("Введите название курса который хотите удалить: ");
        String courseTitle = getTitle();

        courseService.deleteCourse(courseTitle);
        System.out.println("Курс был успешно удалён!\n");
    }

}
