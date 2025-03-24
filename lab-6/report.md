# Порождающие паттерны

## 1) Spring-way фабрика - аналог фабрики для Spring фреймворка

``` java
@Configuration
@RequiredArgsConstructor
public class BotCreation {
    private final BotConfig botConfig;

    @Bean
    public TelegramBot telegramBot() {
        return new TelegramBot(botConfig.telegramToken());
    }

    @Bean
    public RestClient restClient() {
        return RestClient.create(botConfig.baseUrl());
    }
}
```



Теперь нам не нужно в каждом классе создавать экземпляры BotConfig и RestClient. Spring сделает это за нас
![image](https://github.com/user-attachments/assets/9fa4bb34-80f2-451c-b0c5-ee7242f41a73)

UML

![image](https://github.com/user-attachments/assets/198fed91-2be4-4d26-9110-e2c6581bf5be)

## 2) Lombok Builder

``` java
public record ApiErrorResponseDTO(String description, String code, String exceptionName, String exceptionMessage, List<String> stacktrace) {
    public ApiErrorResponseDTO(String description, String code, String exceptionName, String exceptionMessage, List<String> stacktrace) {
        this.description = description;
        this.code = code;
        this.exceptionName = exceptionName;
        this.exceptionMessage = exceptionMessage;
        this.stacktrace = stacktrace;
    }

    public static @NonNull ApiErrorResponseDTOBuilder builder() {
        return new ApiErrorResponseDTOBuilder();
    }

    public String description() {
        return this.description;
    }

    public String code() {
        return this.code;
    }

    public String exceptionName() {
        return this.exceptionName;
    }

    public String exceptionMessage() {
        return this.exceptionMessage;
    }

    public List<String> stacktrace() {
        return this.stacktrace;
    }


    public static class ApiErrorResponseDTOBuilder {

        private String description;

        private String code;

        private String exceptionName;

        private String exceptionMessage;

        private List<String> stacktrace;

        ApiErrorResponseDTOBuilder() {
        }

        public @NonNull ApiErrorResponseDTOBuilder description(final String description) {
            this.description = description;
            return this;
        }
        public @NonNull ApiErrorResponseDTOBuilder code(final String code) {
            this.code = code;
            return this;
        }

        public @NonNull ApiErrorResponseDTOBuilder exceptionName(final String exceptionName) {
            this.exceptionName = exceptionName;
            return this;
        }

        public @NonNull ApiErrorResponseDTOBuilder exceptionMessage(final String exceptionMessage) {
            this.exceptionMessage = exceptionMessage;
            return this;
        }

        public @NonNull ApiErrorResponseDTOBuilder stacktrace(final List<String> stacktrace) {
            this.stacktrace = stacktrace;
            return this;
        }

        public @NonNull ApiErrorResponseDTO build() {
            return new ApiErrorResponseDTO(this.description, this.code, this.exceptionName, this.exceptionMessage, this.stacktrace);
        }
    }
```

Можно билдить DTO

``` java
    public ResponseEntity<ApiErrorResponseDTO> handleInvalid(Exception ex) {
        ApiErrorResponseDTO errorResponse = ApiErrorResponseDTO.builder()
            .description("Некорректные параметры запроса")
            .code(client400)
            .exceptionName(ex.getClass().getName())
            .exceptionMessage(ex.getMessage())
            .stacktrace(ExceptionUtils.getStacktrace(ex))
            .build();

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }
```

UML

![image](https://github.com/user-attachments/assets/61a42d2d-8ba4-400d-a90a-1feab557064e)

## 3) Singleton

``` java
public class TrackCommand implements Command {
    private static volatile TrackCommand instance;
    
    private TrackCommand() {
        this.bot = new TelegramBot("YOUR_BOT_TOKEN");
        this.trackClient = new TrackClient(new BotConfig("TOKEN", "BASE_URL"));

        this.userStates = new ConcurrentHashMap<>();
        this.userUrl = new ConcurrentHashMap<>();
        this.linkTags = new ConcurrentHashMap<>();
        this.linkFilters = new ConcurrentHashMap<>();
    }

    public static TrackCommand getInstance() {
        if (instance == null) {
            synchronized (TrackCommand.class) {
                if (instance == null) {
                    instance = new TrackCommand();
                }
            }
        }
        return instance;
    }

    private final Map<Long, State> userStates;
    private final Map<Long, String> userUrl;
    private final Map<Long, Map<String, List<String>>> linkTags;
    private final Map<Long, Map<String, List<String>>> linkFilters;
    private final TelegramBot bot;
    private final TrackClient trackClient;

    @Override
    public void execute(Long chatId, String message) {
        // ... оригинальная реализация метода execute ...
    }

    private void startHandle(Long chatId) {/*...*/}
    private void waitingForUrlHandle(Long chatId, String message) {/*...*/}
    private void waitingForTags(Long chatId, String message) {/*...*/}
    private void waitingForFilters(Long chatId, String message) {/*...*/}
}
```

UML

![image](https://github.com/user-attachments/assets/152d4d30-12b7-4c45-9c0f-242bca5f6614)


# Структурные паттерны 
## 1) Фасад

``` java
@Component
@RequiredArgsConstructor
public class BotInteractionFacade {
    private final TrackCommand trackCommand;
    private final UntrackCommand untrackCommand;
    private final CommandContainer commandContainer;

    public void handleUpdate(Update update) {
        Long chatId = update.message().chat().id();
        String messageText = update.message().text();

        State currentTrackState = trackCommand.userStates().getOrDefault(chatId, State.START);
        State currentUntrackState = untrackCommand.userStates().getOrDefault(chatId, State.START);

        if (currentTrackState != State.START) {
            trackCommand.execute(chatId, messageText);
            return;
        }

        if (currentUntrackState != State.START) {
            untrackCommand.execute(chatId, messageText);
            return;
        }

        if (messageText != null) {
            commandContainer.retrieveCommand(messageText.trim()).execute(chatId, messageText);
        }
    }

}
```

``` java
@Service
@RequiredArgsConstructor
@Slf4j
@SuppressWarnings("ReturnCount")
public class TelegramBotService {

    private final TelegramBot bot;

    private final BotInteractionFacade botInteractionFacade;

    @PostConstruct
    public void startListening() {
        bot.setUpdatesListener(updates -> {
            for (Update update : updates) {
                if (update.message().text() != null) {
                    log.atInfo()
                            .addKeyValue("chatId", update.message().chat().id())
                            .addKeyValue("userMessage", update.message().text())
                            .setMessage("Пришло сообщение")
                            .log();
                    botInteractionFacade.handleUpdate(update);
                }
            }
            return UpdatesListener.CONFIRMED_UPDATES_ALL;
        });
    }

}
```

UML

![image](https://github.com/user-attachments/assets/2df50d44-8293-4cac-a0f8-dc027307b06b)

## 2) Декоратор

```java
public interface Command {
    void execute(Long chatId, String message);
}
```

```java
@Slf4j
@RequiredArgsConstructor
public class LoggingCommandDecorator implements Command {
    private final Command decoratedCommand;

    @Override
    public void execute(Long chatId, String message) {
        log.info("Executing command for chat {}: {}", chatId, message);
        decoratedCommand.execute(chatId, message);
        log.info("Command executed for chat {}", chatId);
    }
}
```

```java
@Component
public class CommandContainer {
    private final Map<String, Command> commandMap;
    private final UnknownCommand unknownCommand;

    public CommandContainer(
            StartCommand startCommand,
            ListCommand listCommand,
            HelpCommand helpCommand,
            UnknownCommand unknownCommand,
            TrackCommand trackCommand,
            UntrackCommand untrackCommand) {
        commandMap = new HashMap<>();
        commandMap.put(START.commandName(), startCommand);
        commandMap.put(LIST.commandName(), listCommand);
        commandMap.put(HELP.commandName(), helpCommand);
        commandMap.put(TRACK.commandName(), trackCommand);
        commandMap.put(UNTRACK.commandName(), untrackCommand);
        this.unknownCommand = unknownCommand;
    }

    public Command retrieveCommand(String commandIdentifier) {
        Command original = commandMap.getOrDefault(commandIdentifier, unknownCommand);
        return new LoggingCommandDecorator(original);
    }
}
```

UML

![image](https://github.com/user-attachments/assets/cfd5f4b4-b0e4-469f-bb19-6930bdba2905)

## 3) Компоновщик

```java
public interface LinkComponent {
    void checkForUpdates();
}
```
```java
@Component
@RequiredArgsConstructor
public class GithubLinkComponent implements LinkComponent {
    private final LinkRepository linkRepository;
    private final UpdateLinkClient updateLinkClient;
    private final GitHubInfoClient gitHubInfoClient;

    @Override
    public void checkForUpdates() {
        Map<Long, Map<String, LocalDateTime>> links = linkRepository.getAllGithubLinks();

        for (Map.Entry<Long, Map<String, LocalDateTime>> idEntry : links.entrySet()) {
            for (Map.Entry<String, LocalDateTime> urlEntry : idEntry.getValue().entrySet()) {
                LocalDateTime lastSavedTime = urlEntry.getValue();
                LocalDateTime lastUpdatedTime = gitHubInfoClient.getLastUpdatedTime(urlEntry.getKey());

                if (!lastSavedTime.isEqual(lastUpdatedTime)) {
                    updateLinkClient.sendUpdate(idEntry.getKey(), urlEntry.getKey());
                    urlEntry.setValue(lastUpdatedTime);
                }
            }
        }
    }
}
```
```java
@Component
@RequiredArgsConstructor
public class StackOverflowLinkComponent implements LinkComponent{
    private final LinkRepository linkRepository;
    private final StackOverflowClient stackOverflowClient;
    private final UpdateLinkClient updateLinkClient;

    @Override
    public void checkForUpdates() {
        Map<Long, Map<String, Integer>> links = linkRepository.getAllStackOverflowLinks();

        for (Map.Entry<Long, Map<String, Integer>> idEntry : links.entrySet()) {
            for (Map.Entry<String, Integer> urlEntry : idEntry.getValue().entrySet()) {
                Integer lastSavedAnswersCount = urlEntry.getValue();
                Integer lastUpdatedAnswersCount = stackOverflowClient.getLastUpdatedAnswersCount(urlEntry.getKey());

                if (!Objects.equals(lastSavedAnswersCount, lastUpdatedAnswersCount)) {
                    updateLinkClient.sendUpdate(idEntry.getKey(), urlEntry.getKey());
                    urlEntry.setValue(lastUpdatedAnswersCount);
                }
            }
        }
    }
}
```

```java
@Component
@RequiredArgsConstructor
public class LinkComposite implements LinkComponent {
    private final List<LinkComponent> linkComponents;

    @Override
    public void checkForUpdates() {
        linkComponents.forEach(LinkComponent::checkForUpdates);
    }
}
```

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class LinkCheckService {
    private final LinkComposite linkComposite;

    @Scheduled(fixedRate = 15000)
    public void checkForUpdates() {
        log.info("Проверка обновлений началась");
        linkComposite.checkForUpdates();
    }
}
```
UML

![image](https://github.com/user-attachments/assets/537d3965-e6bf-4920-9712-5e4b525baea7)

Можно добавлять новые типы ссылок без изменения существующего кода

## 4) Адаптер

```java
// Сторонний класс, который нельзя изменить
public class LegacyLinkAnalyzer {
    public String fetchMetadata(String url, String apiKey) {
        // Возвращает метаданные в формате "type;timestamp;count"
        return "github;2023-10-01T12:00:00;0";
    }

    public boolean validateUrl(String url) {
        return url.matches("^(https?://)(github|stackoverflow).*");
    }
}
```

```java
@Component
@RequiredArgsConstructor
public class LegacyLinkAnalyzerAdapter implements LinkUpdater {
    private final LegacyLinkAnalyzer legacyAnalyzer;
    private final ScrapperConfig config;

    @Override
    public void checkUpdates(Long chatId, String link) {
        // Используем legacy-метод для получения данных
        String metadata = legacyAnalyzer.fetchMetadata(link, config.stackOverflow().key());
        String[] parts = metadata.split(";");
        
        // Преобразуем данные в ваш формат
        if (parts[0].equals("github")) {
            LocalDateTime updatedTime = LocalDateTime.parse(parts[1]);
            // Логика обновления через ваш сервис...
        } else {
            int answersCount = Integer.parseInt(parts[2]);
            // Логика обновления через ваш сервис...
        }
    }
}
```

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class LinkCheckService {
    private final LinkRepository linkRepository;
    private final UpdateLinkClient updateLinkClient;
    private final LegacyLinkAnalyzerAdapter legacyAdapter; // Внедряем адаптер

    @Scheduled(fixedRate = 15000)
    public void checkForGithubUpdates() {
        linkRepository.getAllGithubLinks().forEach((chatId, links) -> {
            links.forEach((link, lastUpdated) -> {
                legacyAdapter.checkUpdates(chatId, link); // Используем адаптер
            });
        });
    }
}
```

UML

![image](https://github.com/user-attachments/assets/e10b5207-1eac-4dad-8833-20d116f36cb7)


# Поведенческие
## 1) Цепочка обязанностей
``` java
public abstract class StateHandler {
    private StateHandler next;

    public StateHandler setNext(StateHandler next) {
        this.next = next;
        return next;
    }

    public void handle(Long chatId, String message, State state, HandlerContext context) {
        if (canHandle(state)) {
            process(chatId, message, context);
        } else if (next != null) {
            next.handle(chatId, message, state, context);
        }
    }

    protected abstract boolean canHandle(State state);
    protected abstract void process(Long chatId, String message, HandlerContext context);
}
```
```java
public class StartHandler extends StateHandler {
    @Override
    protected boolean canHandle(State state) {
        return state == State.START;
    }

    @Override
    protected void process(Long chatId, String message, HandlerContext context) {
        context.bot().execute(new SendMessage(chatId, "Введите URL для отслеживания (см. /help)"));
        context.userStates().put(chatId, State.WAITING_FOR_URL);
    }
}
```
```java
public class UrlHandler extends StateHandler {
    @Override
    protected boolean canHandle(State state) {
        return state == State.WAITING_FOR_URL;
    }

    @Override
    protected void process(Long chatId, String message, HandlerContext context) {
        if (message.trim().equals("/stop")) {
            context.userStates().put(chatId, State.START);
            context.bot().execute(new SendMessage(chatId, "Вы вышли из меню ввода ссылки"));
            return;
        }

        if (RegexCheck.checkApi(message)) {
            context.userUrl().put(chatId, message);
            context.userStates().put(chatId, State.WAITING_FOR_TAGS);
            context.bot().execute(new SendMessage(chatId, "Введите теги (опционально).\nЕсли теги не нужны - введите /skip"));
        } else {
            context.bot().execute(new SendMessage(chatId, "Некорректно введена ссылка, введите заново, либо введите /stop"));
        }
    }
}
```

```java
public class TagsHandler extends StateHandler {
    @Override
    protected boolean canHandle(State state) {
        return state == State.WAITING_FOR_TAGS;
    }

    @Override
    protected void process(Long chatId, String message, HandlerContext context) {
        if (!message.equals(skip)) {
            context.linkTags().computeIfAbsent(chatId, k -> new ConcurrentHashMap<>())
                .put(context.userUrl().get(chatId), new ArrayList<>(List.of(message.split(" "))));
        }
        context.userStates().put(chatId, State.WAITING_FOR_FILTERS);
        context.bot().execute(new SendMessage(
            chatId,
            "Введите фильтры (опционально, например, user:dummy)\nЕсли фильтры не нужны - введите /skip"
        ));
    }
}
```

```java
public class FiltersHandler extends StateHandler {
    @Override
    protected boolean canHandle(State state) {
        return state == State.WAITING_FOR_FILTERS;
    }

    @Override
    protected void process(Long chatId, String message, HandlerContext context) {
        boolean isSkip = message.equals(skip);
        boolean isValidFilter = RegexCheck.checkFilter(message);

        if (isSkip || isValidFilter) {
            context.userStates().put(chatId, State.START);

            Map<String, List<String>> urlTags = context.linkTags().computeIfAbsent(chatId, k -> new ConcurrentHashMap<>());
            ArrayList<String> tags = (ArrayList<String>) urlTags.computeIfAbsent(context.userUrl().get(chatId), k -> new ArrayList<>());

            Map<String, List<String>> urlFilters = context.linkFilters().computeIfAbsent(chatId, k -> new ConcurrentHashMap<>());
            List<String> filters;

            if (isSkip) {
                filters = urlFilters.computeIfAbsent(context.userUrl().get(chatId), k -> new ArrayList<>());
            } else {
                filters = new ArrayList<>(Arrays.asList(message.split(" ")));
                urlFilters.put(context.userUrl().get(chatId), filters);
            }

            context.bot().execute(new SendMessage(
                chatId,
                context.trackClient().trackLink(chatId, context.userUrl().get(chatId), tags, filters)
            ));
        } else {
            context.bot().execute(new SendMessage(chatId, "Введите фильтры в формате filter:filter"));
        }
    }
}
```

```java
@Getter
public class HandlerContext {
    private final Map<Long, State> userStates;
    private final Map<Long, String> userUrl;
    private final Map<Long, Map<String, List<String>>> linkTags;
    private final Map<Long, Map<String, List<String>>> linkFilters;
    private final TelegramBot bot;
    private final TrackClient trackClient;

    public HandlerContext(
        Map<Long, State> userStates,
        Map<Long, String> userUrl,
        Map<Long, Map<String, List<String>>> linkTags,
        Map<Long, Map<String, List<String>>> linkFilters,
        TelegramBot bot,
        TrackClient trackClient
    ) {
        this.userStates = userStates;
        this.userUrl = userUrl;
        this.linkTags = linkTags;
        this.linkFilters = linkFilters;
        this.bot = bot;
        this.trackClient = trackClient;
    }
}
```

```java
@Component
@Getter
@Slf4j
@SuppressWarnings("MissingSwitchDefault")
public class TrackCommand implements Command {
    private final Map<Long, State> userStates = new ConcurrentHashMap<>();
    private final Map<Long, String> userUrl = new ConcurrentHashMap<>();
    private final Map<Long, Map<String, List<String>>> linkTags = new ConcurrentHashMap<>();
    private final Map<Long, Map<String, List<String>>> linkFilters = new ConcurrentHashMap<>();

    private final TelegramBot bot;
    private final TrackClient trackClient;
    private final HandlerContext context;
    private StateHandler chain;

    public TrackCommand(TelegramBot bot, TrackClient trackClient) {
        this.bot = bot;
        this.trackClient = trackClient;

        context = new HandlerContext(
            userStates,
            userUrl,
            linkTags,
            linkFilters,
            bot,
            trackClient
        );

        StartHandler startHandler = new StartHandler();
        UrlHandler urlHandler = new UrlHandler();
        TagsHandler tagsHandler = new TagsHandler();
        FiltersHandler filtersHandler = new FiltersHandler();

        startHandler.setNext(urlHandler)
            .setNext(tagsHandler)
            .setNext(filtersHandler);

        this.chain = startHandler;
    }

    @Override
    public void execute(Long chatId, String message) {
        State currentState = userStates.getOrDefault(chatId, State.START);
        chain.handle(chatId, message, currentState, context);
    }
}
```
UML

![image](https://github.com/user-attachments/assets/5bd5b89f-82c0-42c3-900a-7ef1f5443ba6)

## 2) Command Pattern

```java
public class TelegramBotService {

    private final TelegramBot bot;
    private final CommandContainer commandContainer;
    private final TrackCommand trackCommand;
    private final UntrackCommand untrackCommand;

    @PostConstruct
    public void startListening() {
        bot.setUpdatesListener(updates -> {
            for (Update update : updates) {
                if (update.message().text() != null) {
                    log.atInfo()
                            .addKeyValue("chatId", update.message().chat().id())
                            .addKeyValue("userMessage", update.message().text())
                            .setMessage("Пришло сообщение")
                            .log();
                    handleMessage(update);
                }
            }
            return UpdatesListener.CONFIRMED_UPDATES_ALL;
        });
    }

    public void handleMessage(Update update) {
        Long chatId = update.message().chat().id();
        String messageText = update.message().text();

        State currentTrackState = trackCommand.userStates().getOrDefault(chatId, State.START);
        State currentUntrackState = untrackCommand.userStates().getOrDefault(chatId, State.START);

        if (currentTrackState != State.START) {
            trackCommand.execute(chatId, messageText);
            return;
        }

        if (currentUntrackState != State.START) {
            untrackCommand.execute(chatId, messageText);
            return;
        }

        if (messageText != null) {
            commandContainer.retrieveCommand(messageText.trim()).execute(chatId, messageText);
        }
    }
}
```

```java
@Component
public class CommandContainer {
    private final Map<String, Command> commandMap;
    private final UnknownCommand unknownCommand;

    public CommandContainer(
            StartCommand startCommand,
            ListCommand listCommand,
            HelpCommand helpCommand,
            UnknownCommand unknownCommand,
            TrackCommand trackCommand,
            UntrackCommand untrackCommand) {
        commandMap = new HashMap<>();
        commandMap.put(START.commandName(), startCommand);
        commandMap.put(LIST.commandName(), listCommand);
        commandMap.put(HELP.commandName(), helpCommand);
        commandMap.put(TRACK.commandName(), trackCommand);
        commandMap.put(UNTRACK.commandName(), untrackCommand);
        this.unknownCommand = unknownCommand;
    }

    public Command retrieveCommand(String commandIdentifier) {
        return commandMap.getOrDefault(commandIdentifier, unknownCommand);
    }
}
```

```java
public interface Command {
    void execute(Long chatId, String message);
}
```

```java
@RequiredArgsConstructor
@Component
@Slf4j
public class StartCommand implements Command {
    private final RegistrationClient registrationClient;
    private final TelegramBot bot;

    @Override
    public void execute(Long chatId, String message) {
        log.atInfo()
                .addKeyValue("chatId", chatId)
                .setMessage("Выполняется команда /start")
                .log();
        bot.execute(new SendMessage(chatId, registrationClient.registerUser(chatId)));
    }
}
```
UML

![image](https://github.com/user-attachments/assets/2d223a66-99bc-496e-9416-d87569304d2e)

## 3) Шаблонный метод

``` java
public abstract class LinkUpdateTemplate {
    protected abstract Object fetchData(String link);
    protected abstract boolean hasUpdates(Object newData, Object storedData);

    public final void checkAndUpdate(Long chatId, String link, LinkRepository repo) {
        Object newData = fetchData(link);
        Object storedData = repo.getData(chatId, link);
        if (hasUpdates(newData, storedData)) {
            repo.updateData(chatId, link, newData);
            // Отправка уведомления...
        }
    }
}

@Component
@RequiredAllArgsConstructor
public class GitHubUpdateTemplate extends LinkUpdateTemplate {
    private GithubInfoClient gitHubInfoClient;

    @Override
    protected Object fetchData(String link) {
        return gitHubInfoClient.getLastUpdatedTime(link);
    }

    @Override
    protected boolean hasUpdates(Object newData, Object storedData) {
        return !((LocalDateTime) newData).equals((LocalDateTime) storedData);
    }
}

@Component
public class StackOverflowTemplate extends LinkUpdateTemplate {
    private StackOverflowInfoClient stackOverflowInfoClient;

    @Override
    protected Object fetchData(String link) {
        return stackOverflowInfoClient.getQuestionSize();
    }

    @Override
    protected boolean hasUpdates(Object newData, Object storedData) {
         return !((LocalDateTime) newData).equals((LocalDateTime) storedData);
    }
}
```
UML

![image](https://github.com/user-attachments/assets/e25400cd-ba24-4922-a033-aade87bb62a5)


## 4) Посетитель 

```java
public interface LinkVisitor {
    void visitGitHubLink(String link);
    void visitStackOverflowLink(String link);
}

@Component
public class StatisticsVisitor implements LinkVisitor {
    @Override
    public void visitGitHubLink(String link) {
        // Сбор статистики по GitHub
    }

    @Override
    public void visitStackOverflowLink(String link) {
        // Сбор статистики по StackOverflow
    }
}

// В LinkRepository:
public void acceptVisitor(LinkVisitor visitor) {
    githubLinks.forEach((chatId, links) -> links.keySet().forEach(visitor::visitGitHubLink));
    stackOverflowLinks.forEach((chatId, links) -> links.keySet().forEach(visitor::visitStackOverflowLink));
}
```

UML

![image](https://github.com/user-attachments/assets/2e804d0d-8de2-48eb-9eee-353031869a35)

Добавляет операции (аналитика, валидация) без изменения существующих классов

## 5) Хранитель

```java
public class LinkRepositoryMemento {
    private final Map<Long, Map<String, LocalDateTime>> githubSnapshot;
    private final Map<Long, Map<String, Integer>> stackOverflowSnapshot;

    public LinkRepositoryMemento(LinkRepository repo) {
        this.githubSnapshot = new ConcurrentHashMap<>(repo.getAllGithubLinks());
        this.stackOverflowSnapshot = new ConcurrentHashMap<>(repo.getAllStackOverflowLinks());
    }

    public void restore(LinkRepository repo) {
        repo.restoreFromMemento(this);
    }
}

// В LinkRepository:
public LinkRepositoryMemento saveState() {
    return new LinkRepositoryMemento(this);
}

public void restoreFromMemento(LinkRepositoryMemento memento) {
    this.githubLinks = memento.getGithubSnapshot();
    this.stackOverflowLinks = memento.getStackOverflowSnapshot();
}
```
UML

![image](https://github.com/user-attachments/assets/e9aff48d-e84f-434f-8fa5-2dc7989ac356)



# GRASP
## 1 Information Expert
Проблема: Как распределить обязанности между классами, чтобы каждый класс отвечал только за те данные, которыми он владеет?
Решение: Ответственность должна быть назначена классу, который имеет максимум информации для её выполнения.

```java
// RegistrationService знает, как зарегистрировать пользователя, так как управляет данными о регистрации
public class RegistrationService {
    private final RegistrationRepository registrationRepository;

    public void registerUser(Long chatId) {
        if (!registrationRepository.existById(chatId)) {
            registrationRepository.save(chatId);
        }
    }
}
```
Результаты: Уменьшение связанности, повышение согласованности.
Связь с другими паттернами: Используется в сочетании с Low Coupling.

## 2 Creator
Проблема: Как определить, какой класс должен создавать объекты?
Решение: Класс, который содержит или агрегирует данные, должен создавать связанные объекты.

```java
public class CommandContainer {
    private final Map<String, Command> commandMap;

    @Autowired
    public CommandContainer(List<Command> commands, UnknownCommand unknownCommand) {
        commandMap = commands.stream().collect(Collectors.toMap(Command::getName, Function.identity()));
    }
}
```
Результаты: Локализация логики создания объектов.
Связь с другими паттернами: Часто используется с Factory.

## 3 Controller
Проблема: Как обрабатывать системные события и управлять потоком выполнения?
Решение: Использовать отдельный класс для обработки запросов и координации действий.

```java
@Service
public class TelegramBotService {
    public void handleMessage(Update update) {
        Command command = commandContainer.retrieveCommand(messageText.trim());
        command.execute(chatId, messageText);
    }
}
```
Результаты: Разделение логики взаимодействия с пользователем и бизнес-логики.
Связь с другими паттернами: Часто связан с Chain of Responsibility.

## 4 High Cohesion
Проблема: Как избежать «божественных классов», которые делают слишком много?
Решение: Классы должны иметь узкоспециализированные обязанности.

```java
// HelpCommand отвечает только за вывод справки
@Component
public class HelpCommand implements Command {
    @Override
    public void execute(Long chatId, String message) {
        bot.execute(new SendMessage(chatId, BotMessages.HELP_MESSAGE));
    }
}
```
Результаты: Упрощение поддержки и тестирования.
Связь с другими паттернами: Связан с Single Responsibility Principle (SRP).

## 5 Polymorphism
Проблема: Как обрабатывать вариации поведения в зависимости от типа объекта?
Решение: Использовать полиморфизм для разделения разных реализаций.

```java
// Команды реализуют интерфейс Command, обеспечивая полиморфное выполнение
public interface Command {
    void execute(Long chatId, String message);
    String getName();
}
```
Результаты: Упрощение добавления новых типов команд.
Связь с другими паттернами: Основа для Strategy и Command.

## 6 Low Coupling
Проблема: Как уменьшить зависимость между классами, чтобы изменения в одном классе не влияли на другие?
Решение: Классы должны быть слабо связаны, то есть зависеть от минимального числа других классов.

```java
// TelegramBotService зависит только от CommandContainer, а не от конкретных команд
public class TelegramBotService {
    private final CommandContainer commandContainer;

    public void handleMessage(Update update) {
        Command command = commandContainer.retrieveCommand(update.message().text());
        command.execute(update.message().chat().id(), update.message().text());
    }
}
```
Результаты: Упрощение тестирования и модификации.
Связь с другими паттернами: Часто используется с Dependency Injection. (Этот паттерн позволяет снизить зависимость классов от конкретных реализаций объектов. Вместо того, чтобы создавать объекты внутри классов (что делает их сильно связанными с конкретными реализациями), зависимости передаются через конструктор, сеттеры или интерфейсы. Это позволяет легко заменять компоненты без изменений в классе, который их использует.)

## 7 Pure Fabrication 
Проблема: Как распределить обязанности, если ни один из существующих классов не подходит для выполнения задачи?
Решение: Создать искусственный класс, который не относится к предметной области, но решает задачу.

```java
@Component
public class RegexCheck {
    public boolean checkApi(String url) {
        // Логика проверки ссылки
    }
}
```
Результаты: Упрощение основной логики за счет выноса вспомогательных функций.
Связь с другими паттернами: Adapter.

## 8 Indirection
Проблема: Как уменьшить прямую зависимость между классами?
Решение: Ввести промежуточный класс или интерфейс для взаимодействия.

```java
// CommandContainer выступает как промежуточный класс для получения команд
public class CommandContainer {
    private final Map<String, Command> commandMap;

    public Command retrieveCommand(String commandIdentifier) {
        return commandMap.getOrDefault(commandIdentifier, unknownCommand);
    }
}
```
Результаты: Уменьшение связанности между классами.
Связь с другими паттернами: Controller

## 9 Protected Variations
Проблема: Как защитить систему от изменений в одной её части?
Решение: Изолировать изменяющиеся части системы через интерфейсы или абстракции.

```java
public interface Command {
    void execute(Long chatId, String message);
    String getName();
}
```
Результаты: Устойчивость к изменениям.
Связь с другими паттернами: Adapter, Command Pattern.

