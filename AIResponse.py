import time
import openai

# https://app.hyperbolic.xyz/
# Можем юзать мой гпт ключ, там на сто лет хватит

SYSTEM_CONTENT = """Только что тебе пришли сообщения из беседы в мессендежере за день. 
Забудь старый контекст. Начни заново. Напиши пересказ того, о чем общались в беседе за день. 
 Твой пересказ должен вызывать смех у людей. Твой пересказ должен быть смешным.
Пересказ должен состоять примерно из 250 слов, но не более 300 слов. Пересказ должен ОБЯЗАТЕЛЬНО состоять из 5-6 абзацев. НЕ МОЖЕТ БЫТЬ БОЛЬШЕ 7 АБЗАЦЕВ.
Абзацы должны быть примерно 50-70 слов.
 В пересказе должны участвовать только самые интересные моменты за день.
 В пересказе обязательно должны упомянаться имена и фамилии тех, кто
 писал сообщения. Пересказ должен начинаться с 'Сегодня в ПИ общались о'. В пересказе должно быть выделено хотя бы одно сообщение в формате 
 'один из участников признался, что'. В пересказе должны быть маты участников. В пересказе должно быть не менее 4 цитат участников в духе Всеволод сказал 'карамба', Мария ответила 'это так'.
 Не пиши 'что вызвало смех и удивление у других участников' и подобные фразы.
  Последний абзац - подведение итогов всего, что ты написал выше.
  Используй ясный и краткий язык."""

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ6aGFzaDIzMDhAbWFpbC5ydSIsImlhdCI6MTczMzkzNzM1NX0.bL4Fp-C-k3gObuKpNFH4oz68vo4IFdND0RpCHPbMYRs"
BASE_URL = "https://api.hyperbolic.xyz/v1"
MODEL_NAME = "meta-llama/Meta-Llama-3.1-405B-Instruct"
count_bad = 0

# Функция для создания запроса
def create_chat_completion(user_content, system_content=SYSTEM_CONTENT, temperature=0.4, max_tokens=6000):
    client = openai.OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
    )

    chat_completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return chat_completion.choices[0].message.content


# Основная функция
def get_answer(message):
    global count_bad
    while True:
        try:
            response = create_chat_completion(user_content=message)
            return response
        except Exception as e:
            print(f"Ошибка: {e}")
            count_bad += 1
            if count_bad == 5:
                exit()
            time.sleep(5)

